input = [1,12,0,20,8,16]
t = 0
history = [[None, None]] * 30000000
last_val = None
for i in input:
    history[i] = [t, None]
    last_val = i
    t += 1

while t < 30000000:
    prior_0, prior_1 = history[last_val]
    cur = 0 if prior_1 is None else prior_0 - prior_1
    hist_of_cur = history[cur]
    hist_of_cur[1] = hist_of_cur[0]
    hist_of_cur[0] = t
    last_val = cur
    t += 1

print(last_val)



