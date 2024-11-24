import sys
import time

from naoqi import ALProxy


def main(robotIP, port):
	names = list()
	times = list()
	keys = list()

				
	names.append("LAnklePitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[-0.121359, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.409751, [3, -0.516667, 0], [3, 0.566667, 0]], [-0.35, [3, -0.566667, 0], [3, 0, 0]]])
	names.append("LAnkleRoll")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.0153604, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.116564, [3, -0.516667, 0], [3, 0.566667, 0]], [0.00167382, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("LElbowRoll")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[-0.306757, [3, -0.166667, 0], [3, 0.516667, 0]], [-1.30539, [3, -0.516667, 0], [3, 0.383333, 0]], [-0.306757, [3, -0.383333, 0], [3, 0.183333, 0]], [-1.00156, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("LElbowYaw")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[-0.12583, [3, -0.166667, 0], [3, 0.516667, 0]], [0.469363, [3, -0.516667, 0], [3, 0.383333, 0]], [-0.12583, [3, -0.383333, 0.417297], [3, 0.183333, -0.199577]], [-1.38126, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("LHand")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[0.924024, [3, -0.166667, 0], [3, 0.516667, 0]], [0.924024, [3, -0.516667, 0], [3, 0.383333, 0]], [0.924024, [3, -0.383333, 0], [3, 0.183333, 0]], [0.25, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("LHipPitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.0749446, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.761086, [3, -0.516667, 0], [3, 0.566667, 0]], [-0.44116, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("LHipRoll")
	times.append([0.5, 2.05, 3.75])
	keys.append([[-0.0477461, [3, -0.166667, 0], [3, 0.516667, 0]], [0.028954, [3, -0.516667, 0], [3, 0.566667, 0]], [0, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("LHipYawPitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.0291025, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.319116, [3, -0.516667, 0], [3, 0.566667, 0]], [0.0031713, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("LKneePitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.0855841, [3, -0.166667, 0], [3, 0.516667, 0]], [1.0474, [3, -0.516667, 0], [3, 0.566667, 0]], [0.699999, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("LShoulderPitch")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[2.0417, [3, -0.166667, 0], [3, 0.516667, 0]], [2.06319, [3, -0.516667, 0], [3, 0.383333, 0]], [2.0417, [3, -0.383333, 0.0214849], [3, 0.183333, -0.0102754]], [1.40101, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("LShoulderRoll")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[0.417205, [3, -0.166667, 0], [3, 0.516667, 0]], [0.246933, [3, -0.516667, 0], [3, 0.383333, 0]], [0.417205, [3, -0.383333, 0], [3, 0.183333, 0]], [0.30903, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("LWristYaw")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[-0.998676, [3, -0.166667, 0], [3, 0.516667, 0]], [-1.01708, [3, -0.516667, 0], [3, 0.383333, 0]], [-0.998676, [3, -0.383333, -0.018408], [3, 0.183333, 0.00880384]], [-0.00181738, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("RAnklePitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[-0.102805, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.543063, [3, -0.516667, 0], [3, 0.566667, 0]], [-0.35, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("RAnkleRoll")
	times.append([0.5, 2.05, 3.75])
	keys.append([[-0.00456227, [3, -0.166667, 0], [3, 0.516667, 0]], [0.135032, [3, -0.516667, 0], [3, 0.566667, 0]], [0.00303459, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("RElbowRoll")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[0.435699, [3, -0.166667, 0], [3, 0.516667, 0]], [1.27786, [3, -0.516667, 0], [3, 0.383333, 0]], [0.435699, [3, -0.383333, 0], [3, 0.183333, 0]], [1.00286, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("RElbowYaw")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[0.222388, [3, -0.166667, 0], [3, 0.516667, 0]], [0.374254, [3, -0.516667, 0], [3, 0.383333, 0]], [0.222388, [3, -0.383333, 0], [3, 0.183333, 0]], [1.38788, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("RHand")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[0.917842, [3, -0.166667, 0], [3, 0.516667, 0]], [0.469091, [3, -0.516667, 0], [3, 0.383333, 0]], [0.917842, [3, -0.383333, 0], [3, 0.183333, 0]], [0.25, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("RHipPitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.041361, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.65354, [3, -0.516667, 0], [3, 0.566667, 0]], [-0.441725, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("RHipRoll")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.0168944, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.0444656, [3, -0.516667, 0], [3, 0.566667, 0]], [0.00789664, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("RKneePitch")
	times.append([0.5, 2.05, 3.75])
	keys.append([[0.103898, [3, -0.166667, 0], [3, 0.516667, 0]], [1.03657, [3, -0.516667, 0], [3, 0.566667, 0]], [0.699999, [3, -0.566667, 0], [3, 0, 0]]])

	names.append("RShoulderPitch")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[1.06617, [3, -0.166667, 0], [3, 0.516667, 0]], [0.943452, [3, -0.516667, 0], [3, 0.383333, 0]], [1.06617, [3, -0.383333, -0.102537], [3, 0.183333, 0.0490393]], [1.39818, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("RShoulderRoll")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[-0.398883, [3, -0.166667, 0], [3, 0.516667, 0]], [-0.0429939, [3, -0.516667, 0], [3, 0.383333, 0]], [-0.398883, [3, -0.383333, 0], [3, 0.183333, 0]], [-0.303682, [3, -0.183333, 0], [3, 0, 0]]])

	names.append("RWristYaw")
	times.append([0.5, 2.05, 3.2, 3.75])
	keys.append([[0.949504, [3, -0.166667, 0], [3, 0.516667, 0]], [0.964844, [3, -0.516667, 0], [3, 0.383333, 0]], [0.949504, [3, -0.383333, 0.0153397], [3, 0.183333, -0.0073364]], [0.0017279, [3, -0.183333, 0], [3, 0, 0]]])

	try:
		motion = ALProxy("ALMotion",robotIP, port)
		motion.angleInterpolationBezier(names, times, keys)
		posture = ALProxy("ALRobotPosture", robotIP, port)
		#posture.goToPosture("StandInit", 1.0)
	except BaseException, err:
		print err


if __name__ == "__main__":
	robotIP = "127.0.0.1"
	port = 9559

	if len(sys.argv) <= 1:
		print "(robotIP default: 127.0.0.1)"
	elif len(sys.argv) <= 2:
		robotIP = sys.argv[1]
	else:
		port = int(sys.argv[2])
		robotIP = sys.argv[1]

	start = time.time()
	main(robotIP, port)
	end = time.time()
	print ("%.2f seconds elapsed" % (end-start))

