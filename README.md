# boxes
Binary tile game simulator and solver

## To Do

1. Understand why the new neighbor_score makes things worse.  See currently failing test.

2. Understand better how to score waves.  Current just adding together everything but
the highest.  This causes a test failure when used with the new neighbor_score.
Tried taking off the highest if it's on the edge and doubling the center value to
address tht issue, but that made the overall behavior much worse.

Also wondering if Need to add a penalty for cases where the middle two
values are equal, but higher than either end.  E.g., 2,4,4,2.  There's
also a case for something like 8,2,2,8.  But note that 4,2,2,4 is not
bad at all.  Overall adding the following code made things worse.

  if len(trim) == 4 and trim[1] == trim[2]: # X,Y,Y,Z
      trim[1] += trim.pop(2)
  while trim[0] == trim[1]:
      trim.pop(0)
      if len(trim) <= 2:
          return 0
  while trim[-1] == trim[-2]:
      trim.pop()
      if len(trim) <= 2:
          return 0

3. Add game logging and undo.

4. Need to project forward more than just the next move.  This may handle
the guaranteed next move logic.  Currently evaluating a single move.
Need to evaluate a single move, random placement of another tile (all
possibilities), evaulate the remainig moves.  Keep the best from each
option.  Average across the options.
