
# #studentID:22195603
# main.py -This is the main file. You run this one to start everything. It has the main loop for the simulation and draws the park window.
#4.0 main simulation file

import argparse
import random
import importlib.util

from park import Park
from utils import load_rides_from_csv

miss = []
if not importlib.util.find_spec("numpy"):
    miss.append("numpy")

if importlib.util.find_spec("matplotlib"):
    import matplotlib
    matplotlib.use('TkAgg') 
    

    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
else:
    plt = None
    FuncAnimation = None
    miss.append("matplotlib")

if miss:
    print(f"!!!!!!missing modules!!!: {', '.join(miss)}")
#4.1 running the simulation
def run_simulation(park: Park, max_patrons: int, steps: int, nogui: bool):
    
    if nogui:
        for i in range(steps):
            if len(park.patrons) < max_patrons:
                park.spawn_patron()
            park.step()
            if i % 20 == 0:
                print(f"Step {park.time}, Patrons: {len(park.patrons)}")
    else:
        fig, ax = plt.subplots(figsize=(12, 8))
        def update(frame):
            ax.clear()
            if len(park.patrons) < max_patrons:
                park.spawn_patron()
            park.step()
            ax.set_facecolor('lightgreen')
            for ride in park.rides:
                ride.draw(ax)
            px = []
            for p in park.patrons:
                px.append(p.x)
            py = []
            for p in park.patrons:
                py.append(p.y)
            ax.scatter(px, py, s=10, c='blue', alpha=0.8)
            ax.set_xlim(0, park.width)
            ax.set_ylim(0, park.height)
            ax.set_aspect('equal', adjustable='box')
            ax.set_title(f"Theme Park Simulation | Time: {park.time} | Patrons: {len(park.patrons)}")
        
        
        anim = FuncAnimation(fig, update, frames=steps, interval=50, repeat=False)
        plt.show()

def main():
#4.2 argument parsing and setup
    parser = argparse.ArgumentParser(description="A simple theme park simulation.")
    parser.add_argument("map_file", nargs='?', default="map.csv",
                        help="Path to the CSV file defining the park layout. Defaults to 'map.csv'")
    parser.add_argument("--steps", type=int, default=1000, help="Number of simulation steps to run.")
    parser.add_argument("--patrons", type=int, default=50, help="Maximum number of patrons in the park.")
    parser.add_argument("--nogui", action="store_true", help="Run in text-only mode without visualization.")
    args = parser.parse_args()

    print("--- Theme Park Simulator ---")
    
   
    park = Park()
    
    rides = load_rides_from_csv(args.map_file)

    if not rides:
        print(f"Error: No rides were loaded from the file '{args.map_file}'. Exiting.")
        return 
    for ride in rides:
        park.add_ride(ride)

   
    print(f"Loaded {len(park.rides)} rides from '{args.map_file}'.")
    print(f"Running simulation for {args.steps} steps with up to {args.patrons} patrons.")
    
   
    run_simulation(park, args.patrons, args.steps, args.nogui)
    
    print("Simulation finished.")


if __name__ == "__main__":
    main()