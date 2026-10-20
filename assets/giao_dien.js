const fmt=n=>Number(n).toFixed(1);const BAD=['Không tìm thấy','Sai ngữ cảnh'];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cards=document.querySelector('#cards'),rows=document.querySelector('#rows');
let sorted=[...candidates],descending=true,activeFilter='all';
const isPriority=c=>!!c.priority;
const vt=v=>v==='Khớp'?'<span class="vt ok">Khớp</span>':BAD.includes(v)?'<span class="vt bad">'+v+'</span>':'<span class="vt na">Chưa kiểm tra</span>';
const flagN=c=>c.criteria.filter(x=>x.flag).length+c.att.signals.filter(s=>BAD.includes(s.ver)).length;
const flagged=candidates.reduce((a,c)=>a+flagN(c),0);
document.querySelector('#stats').innerHTML='<div class="stat"><b>'+candidates.length+'</b><span>CV đã đọc</span></div><div class="stat"><b>'+candidates.filter(c=>c.total>=70&&!c.missing.length).length+'</b><span>hồ sơ từ 70 điểm và đủ tiêu chí bắt buộc</span></div><div class="stat"><b>'+DATAVER.wK+' / '+DATAVER.wS+'</b><span>trọng số K / S (A không chấm điểm)</span></div><div class="stat"><b>'+DATAVER.khop+'/'+DATAVER.tong+'</b><span>câu trích được agent 2 xác nhận khớp · '+flagged+' mục cần rà soát</span></div>';
function render(){
 const visible=sorted.filter(c=>activeFilter==='all'||(activeFilter==='priority'?isPriority(c):!isPriority(c)));
 cards.innerHTML=sorted.filter(isPriority).map((c,i)=>'<article class="card'+(i===0?' featured':'')+'" tabindex="0" data-open="'+c.key+'"><div class="cardtop"><span class="tag '+(i?'secondary':'')+'">'+c.priority+'</span><span class="index">'+String(i+1).padStart(2,'0')+'</span></div><h3>'+esc(c.name)+'</h3><div class="role">'+esc(c.role)+'</div><div class="total">'+fmt(c.total)+'<small> / 100</small></div><div class="signals">'+c.signals.map(s=>'<span class="signal">'+esc(s)+'</span>').join('')+'</div><div class="verify"><b>Cần xác minh:</b> '+esc(c.verify)+(c.total<70?' · <b>Cần làm rõ trước</b>':'')+'</div></article>').join('');
 rows.innerHTML=visible.map(c=>'<tr data-open="'+c.key+'"'+(flagN(c)?' class="flagrow"':'')+'><td>'+esc(c.name)+'</td><td><b>'+fmt(c.total)+'</b></td><td>'+fmt(c.S)+'</td><td>'+fmt(c.K)+'</td><td>'+Math.round(c.coverage*100)+'%</td><td><span class="pill">'+c.level+'</span>'+(c.missing.length?'<br><small>Thiếu bắt buộc: '+c.missing.join(', ')+'</small>':'')+'</td><td>'+(flagN(c)?'<span class="vt bad">'+flagN(c)+' cần rà soát</span>':'<span class="vt ok">Khớp</span>')+'</td></tr>').join('');
 document.querySelectorAll('[data-open]').forEach(el=>{el.addEventListener('click',()=>openCandidate(el.dataset.open));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openCandidate(el.dataset.open)}})});
}
function radarMarkup(c){
 const cx=150,cy=110,r=72,ax=c.criteria.map((x,i)=>({id:x.id,v:x.score/3*100,a:-90+i*360/c.criteria.length}));
 const xy=(s,a)=>{const t=a*Math.PI/180;return [cx+Math.cos(t)*r*s,cy+Math.sin(t)*r*s]};
 const pt=(s,a)=>xy(s,a).map(n=>n.toFixed(1)).join(',');
 const grids=[.25,.5,.75,1].map(s=>'<polygon class="radar-grid" points="'+ax.map(p=>pt(s,p.a)).join(' ')+'"></polygon>').join('');
 const spokes=ax.map(p=>{const q=xy(1,p.a);return '<line class="radar-axis" x1="'+cx+'" y1="'+cy+'" x2="'+q[0].toFixed(1)+'" y2="'+q[1].toFixed(1)+'"></line>'}).join('');
 const dots=ax.map(p=>{const q=xy(p.v/100,p.a);return '<circle class="radar-dot" cx="'+q[0].toFixed(1)+'" cy="'+q[1].toFixed(1)+'" r="4"></circle>'}).join('');
 const labels=ax.map(p=>{const q=xy(1.2,p.a);return '<text class="radar-label" x="'+q[0].toFixed(1)+'" y="'+(q[1]+4).toFixed(1)+'" text-anchor="middle">'+p.id+'</text>'}).join('');
 return '<div class="radarwrap"><svg class="radarsvg" viewBox="0 0 300 220" role="img" aria-label="Biểu đồ mức bằng chứng theo 10 tiêu chí K và S">'+grids+spokes+'<polygon class="radar-area" points="'+ax.map(p=>pt(p.v/100,p.a)).join(' ')+'"></polygon>'+dots+labels+'</svg><div class="radarlegend"><span>S <b>'+fmt(c.S)+'</b></span><span>K <b>'+fmt(c.K)+'</b></span><span>Bao phủ <b>'+Math.round(c.coverage*100)+'%</b></span></div></div>';
}
function blockScores(c){return '<div class="scoreline"><div class="scorebox"><b>'+fmt(c.total)+'</b><span>Điểm tổng / 100</span></div><div class="scorebox"><b>'+fmt(c.S)+'</b><span>S / 100</span></div><div class="scorebox"><b>'+fmt(c.K)+'</b><span>K / 100</span></div></div><div class="coverage">'+Math.round(c.coverage*100)+'% tiêu chí có bằng chứng · '+c.level+'</div>'}
function quotes(x){return (x.quotes||[]).map(q=>'<span class="quote'+(BAD.includes(q.ver)?' bad':'')+'">“'+esc(q.text)+'”'+vt(q.ver)+'<i>'+esc(q.vi_tri)+(BAD.includes(q.ver)&&q.ver_note?' · '+esc(q.ver_note):'')+'</i></span>').join('')}
function items(list){if(!list.length)return '<p class="coverage">Không có.</p>';return list.map(x=>'<div class="criterion'+(x.flag?' flag':'')+'"><div class="criterionhead"><span>'+x.id+' · '+esc(x.text)+(x.priority==='Bắt buộc'?'<em class="req">Bắt buộc</em>':'')+(x.flag?'<span class="vt bad">Cần rà soát</span>':'')+'</span><span>'+x.score+'/3</span></div><small>'+esc(x.evidence)+(x.absence?' '+(x.absence.ver==='Khớp'?'<span class="vt ok">Đã xác nhận CV không nêu</span>':'<span class="vt bad">'+x.absence.ver+'</span> '+esc(x.absence.note)):'')+'</small><div class="evi">'+quotes(x)+'</div></div>').join('')}
function attMarkup(c){return '<div class="attbox"><b>Dấu hiệu hành vi trong CV (không chấm điểm)</b>'+(c.att.signals.length?c.att.signals.map(s=>'<span class="quote'+(BAD.includes(s.ver)?' bad':'')+'"><b>'+esc(s.nhom)+':</b> “'+esc(s.text)+'”'+vt(s.ver)+'<i>'+esc(s.vi_tri)+(BAD.includes(s.ver)&&s.ver_note?' · '+esc(s.ver_note):'')+'</i></span>').join(''):'<p class="coverage">Không tìm thấy dấu hiệu (không phải kết luận tiêu cực).</p>')+'<p class="coverage"><b>Ổn định công việc:</b> '+esc(c.att.stability)+'</p></div>'}
function blobUrl(u){if(!u.startsWith('data:'))return u;const p=u.split(','),m=p[0].match(/:(.*?);/)[1],b=atob(p[1]),a=new Uint8Array(b.length);for(let i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return URL.createObjectURL(new Blob([a],{type:m}))}
function openCandidate(key){const c=candidates.find(x=>x.key===key);if(!c)return;
 document.querySelector('#modalFit').textContent=c.level;document.querySelector('#modalName').textContent=c.name;document.querySelector('#modalRole').textContent=c.role;
 const meets=c.criteria.filter(x=>x.score>0),gaps=c.criteria.filter(x=>x.score===0);
 document.querySelector('#overview').innerHTML=blockScores(c)+'<div class="detailgrid summarygrid"><div class="block radarblock"><h4>Mức bằng chứng theo tiêu chí K/S</h4>'+radarMarkup(c)+'</div><div class="block"><h4>Tóm tắt</h4><p class="coverage">'+esc(c.summary)+'</p><span class="priorityline">'+(c.priority||'Ngoài nhóm ưu tiên')+'</span><h4 style="margin-top:22px">Điểm cần kiểm tra</h4><p class="coverage">'+(c.checks.map(esc).join('<br>')||'Không có')+'</p></div><div class="block wide"><h4>Phù hợp · '+meets.length+'</h4>'+items(meets)+'</div><div class="block wide"><h4>Chưa đủ bằng chứng · '+gaps.length+'</h4>'+items(gaps)+'</div><div class="block wide"><h4>Thái độ: dấu hiệu và câu hỏi hành vi (STAR)</h4>'+attMarkup(c)+'<ol class="list">'+c.att.star.map(q=>'<li>'+esc(q)+'</li>').join('')+'</ol></div><div class="block wide"><h4>Câu hỏi cần xác minh</h4><ol class="list">'+c.questions.map(q=>'<li>'+esc(q)+'</li>').join('')+'</ol></div></div>';
 document.querySelector('#cv').innerHTML='<div class="cvbox"><button class="openbtn" id="openCv">Mở ảnh CV ở tab mới</button><img src="'+c.image+'" alt="CV gốc của '+esc(c.name)+'"></div>';
 document.querySelector('#openCv').addEventListener('click',()=>window.open(blobUrl(c.image),'_blank'));
 setTab('overview');document.querySelector('#modal').showModal();}
function setTab(name){document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.tab===name));document.querySelectorAll('.panel').forEach(p=>p.hidden=p.dataset.panel!==name)}
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>setTab(t.dataset.tab)));
document.querySelector('.close').addEventListener('click',()=>document.querySelector('#modal').close());
document.querySelector('#modal').addEventListener('click',e=>{if(e.target.id==='modal')e.target.close()});
document.querySelectorAll('.filter').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));activeFilter=b.dataset.filter;render()}));
document.querySelector('#sortButton').addEventListener('click',()=>{descending=!descending;sorted.sort((a,b)=>descending?b.total-a.total:a.total-b.total);document.querySelector('#sortButton').textContent='Sắp theo điểm '+(descending?'↓':'↑');render()});
render();
