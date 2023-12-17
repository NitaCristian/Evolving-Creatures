import os
import random
import sys
import time

import numpy as np
import pybullet as p

import creature
import genome


def make_rocks(num_rocks=100, max_size=0.25, arena_size=10):
    for _ in range(num_rocks):
        x = random.uniform(-1 * arena_size / 2, arena_size / 2)
        y = random.uniform(-1 * arena_size / 2, arena_size / 2)
        z = 0.5  # Adjust based on your needs
        size = random.uniform(0.1, max_size)
        orientation = p.getQuaternionFromEuler(
            [random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)])
        rock_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
        rock_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.5, 0.5, 0.5, 1])
        rock_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=rock_shape, baseVisualShapeIndex=rock_visual,
                                      basePosition=[x, y, z], baseOrientation=orientation)


def make_arena(arena_size=10, wall_height=1):
    wall_thickness = 0.5
    floor_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX,
                                                   halfExtents=[arena_size / 2, arena_size / 2, wall_thickness])
    floor_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX,
                                             halfExtents=[arena_size / 2, arena_size / 2, wall_thickness],
                                             rgbaColor=[1, 1, 0, 1])
    floor_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=floor_collision_shape,
                                   baseVisualShapeIndex=floor_visual_shape, basePosition=[0, 0, -wall_thickness])

    wall_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX,
                                                  halfExtents=[arena_size / 2, wall_thickness / 2, wall_height / 2])
    wall_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX,
                                            halfExtents=[arena_size / 2, wall_thickness / 2, wall_height / 2],
                                            rgbaColor=[0.7, 0.7, 0.7, 1])  # Gray walls

    # Create four walls
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape,
                      basePosition=[0, arena_size / 2, wall_height / 2])
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape,
                      basePosition=[0, -arena_size / 2, wall_height / 2])

    wall_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX,
                                                  halfExtents=[wall_thickness / 2, arena_size / 2, wall_height / 2])
    wall_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX,
                                            halfExtents=[wall_thickness / 2, arena_size / 2, wall_height / 2],
                                            rgbaColor=[0.7, 0.7, 0.7, 1])  # Gray walls

    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape,
                      basePosition=[arena_size / 2, 0, wall_height / 2])
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape,
                      basePosition=[-arena_size / 2, 0, wall_height / 2])


# ... usual starter code to create a sim and floor
def main(csv_file):
    assert os.path.exists(csv_file), "Tried to load " + csv_file + " but it does not exists"

    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    # plane_shape = p.createCollisionShape(p.GEOM_PLANE)
    # floor = p.createMultiBody(plane_shape, plane_shape)
    p.setGravity(0, 0, -10)
    #   p.setRealTimeSimulation(1)

    arena_size = 20
    make_arena(arena_size=arena_size)
    # make_rocks(arena_size=arena_size)

    mountain_position = (0, 0, -1)  # Adjust as needed
    mountain_orientation = p.getQuaternionFromEuler((0, 0, 0))
    p.setAdditionalSearchPath('shapes/')
    # mountain = p.loadURDF("mountain.urdf", mountain_position, mountain_orientation, useFixedBase=1)
    # mountain = p.loadURDF("mountain_with_cubes.urdf", mountain_position, mountain_orientation, useFixedBase=1)
    mountain = p.loadURDF("mountain.urdf", mountain_position, mountain_orientation, useFixedBase=1)

    # generate a random creature
    cr = creature.Creature(gene_count=1)
    dna = genome.Genome.from_csv(csv_file)
    cr.update_dna(dna)
    # save it to XML
    with open('models/test.urdf', 'w') as f:
        f.write(cr.to_xml())
    # load it into the sim
    rob1 = p.loadURDF('models/test.urdf')
    # air drop it
    p.resetBasePositionAndOrientation(rob1, [7, 7, 2.5], [0, 0, 0, 1])
    start_pos, orn = p.getBasePositionAndOrientation(rob1)

    # iterate 
    elapsed_time = 0
    wait_time = 1.0 / 240  # seconds
    total_time = 30  # seconds
    step = 0
    while True:
        p.stepSimulation()
        step += 1
        if step % 24 == 0:
            motors = cr.get_motors()
            assert len(motors) == p.getNumJoints(rob1), "Something went wrong"
            for jid in range(p.getNumJoints(rob1)):
                mode = p.VELOCITY_CONTROL
                vel = motors[jid].get_output()
                p.setJointMotorControl2(rob1,
                                        jid,
                                        controlMode=mode,
                                        targetVelocity=vel)
            new_pos, orn = p.getBasePositionAndOrientation(rob1)
            # print(new_pos)
            dist_moved = np.linalg.norm(np.asarray([0, 0, 4]) - np.asarray(new_pos))
            print(dist_moved)
        time.sleep(wait_time)
        elapsed_time += wait_time
        if elapsed_time > total_time:
            break

    print("TOTAL DISTANCE MOVED:", dist_moved)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python playback_test.py csv_filename"
    main(sys.argv[1])
