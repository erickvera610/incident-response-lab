import random
TRANSITIONS = {'Open': ['Investigating'], 'Investigating': ['Resolved'], 'Resolved': ['Closed'], 'Closed': []}

def transition(state, new):
    if new not in TRANSITIONS.get(state, []):
        raise ValueError(f'Invalid transition: {state} to {new}')
    return new

def simulate(seed=42, count=12):
    rng = random.Random(seed)
    incidents = []
    for i in range(count):
        state = 'Open'
        time = 0
        history = [{'state': state, 'minute': 0}]
        for step in range(rng.randint(1, 3)):
            new = ['Investigating', 'Resolved', 'Closed'][step]
            state = transition(state, new)
            time += rng.randint(5, 90)
            history.append({'state': state, 'minute': time})
        incidents.append({'id': i + 1, 'service': ['API', 'Database', 'Web'][i % 3], 'severity': ['High', 'Medium', 'Low'][i % 3], 'state': state, 'history': history})
    times = [next((e['minute'] for e in item['history'] if e['state'] == 'Resolved')) for item in incidents if any((e['state'] == 'Resolved' for e in item['history']))]
    return {'incidents': incidents, 'resolved_count': len(times), 'mean_resolution_minutes': sum(times) / len(times) if times else None}

def run(p):
    count = int(p.get('count', 12))
    if not 1 <= count <= 50:
        raise ValueError('Count must be 1 to 50')
    return {**simulate(int(p.get('seed', 42)), count), 'note': 'Fictional event histories. A learning prototype for software reliability, not a live monitoring system.'}
