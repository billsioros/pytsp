
def orientation(p1, p2, p3):
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


def counterclockwise(p1, p2, p3):
    return orientation(p1, p2, p3) > 0


def between(p1, p2, p3):
    if orientation(p1, p2, p3) != 0:
        return False

    if min(p1[0], p3[0]) > p2[0] or p2[0] > max(p1[0], p3[0]):
        return False

    if min(p1[1], p3[1]) > p2[1] or p2[1] > max(p1[1], p3[1]):
        return False

    return True


def jarvis(points):
    if len(points) < 3:
        return []

    points = sorted(points)

    convex_hull = [points[0]]

    current = None
    while True:
        current = points[0]
        for point in points[1:]:
            if current == convex_hull[-1] or \
                between(convex_hull[-1], current, point) or \
                    counterclockwise(convex_hull[-1], current, point):
                current = point

        if current == convex_hull[0]:
            break

        convex_hull.append(current)

    return convex_hull
