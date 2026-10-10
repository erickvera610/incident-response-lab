const allowedTransitions= {
    Open:['Investigating'],Investigating:['Resolved'],Resolved:['Closed'],Closed:[]
}
;
function loadIncidents() {
    return JSON.parse(localStorage.getItem('incident-lab-v3')||'[]');
}
function saveIncidents(rows) {
    localStorage.setItem('incident-lab-v3',JSON.stringify(rows));
}
function createIncident(p) {
    if(typeof p.title!=='string'||!p.title.trim()||p.title.length>120)throw Error('Title must be 1–120 characters');
    if(!['API','Database','Web'].includes(p.service)||!['High','Medium','Low'].includes(p.severity))throw Error('Unknown service or severity');
    const rows=loadIncidents(),now=new Date().toISOString(),row= {
        id:rows.reduce((m,r)=>Math.max(m,r.id),0)+1,title:p.title.trim(),service:p.service,severity:p.severity,state:'Open',version:1,created_at:now,history:[ {
            state:'Open',version:1,created_at:now
        }
        ],request_keys: {
        }
    }
    ;
    rows.unshift(row);
    saveIncidents(rows);
    return row;
}
function moveIncident(p) {
    const rows=loadIncidents(),row=rows.find(r=>r.id===p.id);
    if(!row)throw Error('Incident not found');
    if(typeof p.request_key!=='string'||!p.request_key||p.request_key.length>100)throw Error('Request key required');
    const prior=row.request_keys[p.request_key];
    if(prior) {
        if(prior.state!==p.state||prior.version!==p.version+1)throw Error('Request key reused with different event');
        return row;
    }
    if(row.version!==p.version)throw Error('Stale version; refresh first');
    if(!allowedTransitions[row.state].includes(p.state))throw Error('Invalid state transition');
    row.state=p.state;
    row.version++;
    row.history.push( {
        state:p.state,version:row.version,created_at:new Date().toISOString()
    }
    );
    row.request_keys[p.request_key]= {
        state:p.state,version:row.version
    }
    ;
    saveIncidents(rows);
    return row;
}
if(typeof module!=='undefined')module.exports= {
    loadIncidents,createIncident,moveIncident
}
;
