import pandas as pd
import json

def build_graph(csv_path='dataset.csv'):
    df = pd.read_csv(csv_path)
    # Ensure order by train and sequence
    df = df.sort_values(by=['Train No.', 'islno'])
    
    graph = {}
    for train_no, group in df.groupby('Train No.'):
        stations = group.to_dict('records')
        for i in range(len(stations) - 1):
            start = str(stations[i]['station Code']).strip().upper()
            end = str(stations[i+1]['station Code']).strip().upper()
            
            edge = {
                "to": end,
                "train_no": str(stations[i]['Train No.']),
                "train_name": stations[i]['train Name'],
                # Use [0:5] to get only the first 5 characters (HH:MM)
                "arrival": str(stations[i]['Arrival time'])[:-3],#[:4], 
                "departure": str(stations[i+1]['Departure time'])[:-3]#[:4]
            }

            if start not in graph: graph[start] = []
            graph[start].append(edge)

    with open('graph.json', 'w') as f:
        json.dump(graph, f, indent=2)
    print("Graph built successfully.")

if __name__ == "__main__":
    build_graph()