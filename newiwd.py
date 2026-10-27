#mdules
import random
import time as Time
import bisect

#globals
J = 0
I = 0
job = [ ]
mesin = [ ]
T = { }
#4-4
# sampleT = {(1, 2): 7, (3, 2): 69, (1, 3): 4, (3, 3): 605, (4, 1): 317, (3, 1): 42, (4, 4): 7, (1, 4): 351, (2, 4): 358, (2, 3): 1, (2, 1): 3, (4, 3): 390, (2, 2): 638, (4, 2): 286, (3, 4): 284, (1, 1): 638}

#7-7
sampleT = {(7, 3): 227, (4, 7): 166, (1, 3): 126, (6, 6): 165, (5, 6): 180, (5, 4): 45, (2, 1): 107, (6, 2): 74, (1, 6): 323, (5, 1): 64, (3, 7): 165, (2, 5): 220, (7, 2): 234, (1, 2): 176, (3, 1): 214, (6, 7): 61, (5, 5): 71, (7, 6): 8, (4, 4): 321, (6, 3): 98, (1, 5): 101, (3, 6): 130, (2, 2): 88, (3, 3): 118, (5, 3): 191, (4, 1): 5, (1, 1): 123, (6, 4): 302, (3, 2): 181, (2, 6): 11, (7, 1): 398, (4, 5): 204, (1, 4): 79, (7, 7): 3, (7, 5): 55, (2, 3): 154, (4, 2): 120, (6, 5): 211, (3, 5): 42, (2, 7): 244, (4, 6): 103, (3, 4): 56, (6, 1): 89, (5, 7): 238, (7, 4): 75, (4, 3): 33, (1, 7): 23, (5, 2): 123, (2, 4): 111}
lower_bound = 1011

#10-10
# sampleT = {(7, 3): 88, (6, 9): 1, (1, 3): 86, (4, 8): 161, (2, 8): 55, (9, 8): 4, (6, 2): 2, (1, 6): 21, (7, 10): 1, (3, 7): 2, (2, 5): 1, (8, 5): 1, (5, 8): 1, (10, 8): 308, (6, 7): 1, (5, 5): 667, (10, 7): 6, (3, 10): 1, (6, 10): 75, (8, 10): 230, (3, 5): 2, (1, 1): 185, (4, 10): 676, (3, 2): 3, (2, 6): 2, (8, 2): 12, (4, 5): 1, (9, 3): 1, (1, 4): 6, (3, 9): 5, (2, 3): 3, (1, 9): 13, (8, 7): 419, (4, 2): 3, (9, 6): 183, (6, 5): 4, (5, 3): 1, (10, 5): 1, (6, 8): 1, (3, 1): 20, (9, 9): 147, (1, 7): 234, (7, 8): 195, (2, 4): 55, (8, 4): 1, (5, 9): 52, (4, 7): 1, (9, 1): 5, (6, 6): 41, (5, 6): 92, (10, 6): 1, (7, 7): 2, (2, 1): 282, (8, 9): 91, (9, 4): 1, (5, 1): 6, (10, 3): 185, (7, 2): 596, (1, 2): 2, (3, 8): 6, (7, 5): 1, (4, 9): 3, (3, 3): 13, (2, 9): 586, (8, 1): 3, (4, 4): 9, (6, 3): 573, (1, 5): 320, (3, 6): 458, (2, 2): 1, (1, 10): 1, (8, 6): 101, (4, 1): 1, (10, 9): 1, (9, 7): 332, (6, 4): 19, (5, 4): 178, (10, 4): 240, (7, 1): 14, (2, 10): 13, (9, 10): 1, (10, 1): 201, (7, 9): 101, (2, 7): 2, (8, 3): 5, (5, 10): 1, (4, 6): 100, (10, 10): 1, (9, 2): 324, (3, 4): 490, (6, 1): 283, (5, 7): 1, (7, 4): 1, (1, 8): 132, (8, 8): 137, (4, 3): 45, (9, 5): 2, (5, 2): 1, (7, 6): 1, (10, 2): 56}

#algo params
initsoil = 1000.0      #soil initial (= soil upper bound; low soil = attractive edge)
soilratio = 50.0       #soil upper bound / soil lower bound (MMAS-style bounds)
epsilon = 0.0001       #epsilon
alpha = 1.0            #exponent on 1/soil in the selection weight
beta = 2.0             #exponent on the heuristic HUD in the selection weight
rhon = 0.1             #local updater: a drop that crosses an edge deposits a little soil there (diversifies the next drops of the same iteration)
rhoiwd = 0.2           #global updater: evaporation rate + erosion rate on the iteration-best and total-best paths
tbweight = 0.5         #share of the global erosion that goes to the total-best path (rest goes to the iteration-best)
stagmax = 8            #iterations without total-best improvement before the soil is reset
LS_BUDGET = 2          #local-search decodes per iteration, as a multiple of N (0 disables local search)
MIRROR = 0             #also try the time-reversed schedule when canonicalising (2 extra decodes per use)
TB_SHARE = 0.25        #share of the local-search budget spent on intensifying the total-best
sideways = 0.3         #probability of accepting an equal-makespan move in local search
HEUR = 'lpt'           #heuristic HUD: 'lpt' (static, op length) or 'ltrp' (dynamic, remaining job+machine work)

N = 100 #waterdropMax
itermax = 500 #iterationMax

nodes = {}
soils = {}

MSTB= 999999
TB= [ ]
STT= { }
FTT= { }

iwdtimes = []
makespantimes = []
lstimes = []

#classes
class Node:
    def __init__(self, job, machine, duration):
        self.job = job
        self.machine = machine
        self.duration = duration
        self.value = (job, machine)

#funcs
def decode(seq):
    """Earliest-gap insertion decoder (active schedule). Returns (makespan, ST, FT).
    Each op is put in the earliest interval that is free on both its job and its machine."""
    jb = {}
    mb = {}
    ST = {}
    FT = {}
    for (j, i) in seq:
        p = T[j, i]
        a = jb.setdefault(j, [])
        b = mb.setdefault(i, [])
        t = 0
        ia = 0
        ib = 0
        while True:
            if ia < len(a) and (ib >= len(b) or a[ia][0] <= b[ib][0]):
                s, f = a[ia]
                ia += 1
            elif ib < len(b):
                s, f = b[ib]
                ib += 1
            else:
                break
            if s - t >= p:
                break
            if f > t:
                t = f
        ST[j, i] = t
        FT[j, i] = t + p
        bisect.insort(a, (t, t + p))
        bisect.insort(b, (t, t + p))
    return max(FT.values()), ST, FT

def canonical(seq, MS, ST, FT):
    """Re-order the sequence by start time and re-decode; keep it if not worse.
    Gives the soil a consistent ordering to learn from."""
    seq2 = sorted(seq, key=lambda op: (ST[op], op))
    MS2, ST2, FT2 = decode(seq2)
    if MS2 <= MS:
        seq, MS, ST, FT = seq2, MS2, ST2, FT2
    if MIRROR:
        # open shop is reversible: decode the reversed sequence, mirror the times, re-decode forward
        MSr, STr, FTr = decode(seq[::-1])
        seq3 = sorted(seq, key=lambda op: (MSr - FTr[op], op))
        MS3, ST3, FT3 = decode(seq3)
        if MS3 < MS:
            seq, MS, ST, FT = seq3, MS3, ST3, FT3
    return seq, MS, ST, FT

def critical_ops(MS, ST, FT):
    """One critical chain: start at an op finishing at the makespan, walk back through the
    job/machine predecessor whose finish equals the current start."""
    byfinish = {}
    for op, f in FT.items():
        byfinish.setdefault(f, []).append(op)
    chain = []
    cur = random.choice(byfinish[MS])
    seen = set()
    while cur is not None and cur not in seen:
        seen.add(cur)
        chain.append(cur)
        preds = [op for op in byfinish.get(ST[cur], []) if op[0] == cur[0] or op[1] == cur[1]]
        cur = random.choice(preds) if preds else None
    return chain

def neighbours(seq, MS, ST, FT):
    """Candidate moves from one critical chain, as (kind, op, target) tuples:
    'before': move op just before its critical predecessor in the sequence (swap their precedence);
    'after' : move op just after its critical successor;
    'rand'  : move op to a random earlier position."""
    chain = critical_ops(MS, ST, FT)
    cand = []
    for k, op in enumerate(chain):
        if k + 1 < len(chain):
            cand.append(('before', op, chain[k + 1]))
        if k > 0:
            cand.append(('after', op, chain[k - 1]))
        cand.append(('rand', op, None))
    random.shuffle(cand)
    return cand

def apply_move(seq, move):
    kind, op, other = move
    pos = {o: k for k, o in enumerate(seq)}
    k = pos[op]
    seq2 = list(seq)
    del seq2[k]
    if kind == 'before':
        newk = pos[other] if pos[other] < k else pos[other] - 1
    elif kind == 'after':
        newk = pos[other] + 1 if pos[other] < k else pos[other]
    else:
        if k == 0:
            return None
        newk = random.randrange(0, k)
    if newk == k:
        return None
    seq2.insert(newk, op)
    return seq2

def local_search(seq, MS, ST, FT, budget):
    """Critical-path guided local search on the sequence, first improvement, sideways moves
    allowed, at most `budget` decodes. Returns the best (seq, MS, ST, FT) found."""
    used = 0
    bestseq, bestMS, bestST, bestFT = seq, MS, ST, FT
    while used < budget:
        improved = False
        for move in neighbours(seq, MS, ST, FT):
            if used >= budget:
                break
            seq2 = apply_move(seq, move)
            if seq2 is None:
                continue
            MS2, ST2, FT2 = decode(seq2)
            used += 1
            if MS2 < MS:
                seq, MS, ST, FT = seq2, MS2, ST2, FT2
                improved = True
                if MS < bestMS:
                    bestseq, bestMS, bestST, bestFT = seq, MS, ST, FT
                break
            if MS2 == MS and random.random() < sideways:
                seq, MS, ST, FT = seq2, MS2, ST2, FT2
                break
        if not improved and used < budget:
            # random perturbation to leave a plateau
            a, b = random.sample(range(len(seq)), 2)
            seq2 = list(seq)
            seq2[a], seq2[b] = seq2[b], seq2[a]
            MS2, ST2, FT2 = decode(seq2)
            used += 1
            if MS2 <= MS:
                seq, MS, ST, FT = seq2, MS2, ST2, FT2
    return bestseq, bestMS, bestST, bestFT

def erode(path, amount):
    """Global update: remove `amount` of the soil range along a directed path (incl. start edge)."""
    prev = 0
    for op in path:
        s = soils[prev, op]
        soils[prev, op] = max(soil_lo, s - amount * (s - soil_lo))
        prev = op

#initialization
print("START INISIALISASI PARAMETER MASALAH")
J = 7
I = 7
startTime = Time.time()
for a in range(1,J+1):
    for b in range(1,I+1):
        job.append(a)
        mesin.append(b)
        node = Node(a, b, int(random.randint(1,250)))
        if (a,b) in sampleT:
            node.duration = sampleT[(a,b)]
        print("node ({},{}) duration: {}".format(node.job, node.machine, node.duration))
        nodes[(a,b)] = node
        T[a,b] = nodes[(a,b)].duration

print("Nodes: {}, length: {}".format(nodes, len(nodes)))
print("duration: ", T)
print("END INISIALISASI PARAMETER MASALAH")
print(" ")

print("START INISIALISASI PARAMETER ALGORITMA")
soil_hi = initsoil
soil_lo = initsoil / soilratio
Tmax = max(T.values())
# HUD: heuristic desirability of visiting an op next = longest-processing-time-first
HUD = {op: (T[op] / Tmax) ** beta for op in nodes}
loadj = {j: sum(T[j, i] for i in range(1, I + 1)) for j in range(1, J + 1)}
loadm = {i: sum(T[j, i] for j in range(1, J + 1)) for i in range(1, I + 1)}
Tsum = float(sum(T.values()))
print("initsoil = {}".format(initsoil))
print("END INISIALISASI PARAMETER ALGORITMA")
print(" ")

#ALGO SET SOIL X,Y = INITSOIL (directed, with a virtual start node 0)
print("START ALGORITMA SET SOIL(X,Y) = INITSOIL DAN SOIL-SOIL LAINNYA")
def reset_soil():
    for key in nodes:
        soils[(0, key)] = soil_hi
        for key2 in nodes:
            if key != key2:
                soils[(key, key2)] = soil_hi
reset_soil()
print("soils length: {}".format(len(soils)))
print("END ALGORITMA SET SOIL(X,Y) = INITSOIL")
print(" ")

#ALGORITMA BESAR
print("START ALGORITMA UMUM")
iterasi = 0
best = 0
stag = 0
ops_all = list(nodes)
n_ops = len(ops_all)

while (MSTB > lower_bound and iterasi < itermax): #Mulai loop buat sekian iterasi
    iterasi += 1
    MSIB= 999999
    IB= [ ]
    STB= { }
    FTB= { }

    for n in range(1, N+1): #Mulai loop buat sekian n
        iwdStart = Time.time()
        current_node = 0
        unfinished = list(ops_all)
        path = []
        if HEUR == 'ltrp':
            remj = dict(loadj)
            remm = dict(loadm)
        while unfinished: #Mulai loop buat ngisi VC
            weights = []
            if HEUR == 'ltrp':
                for city in unfinished:
                    s = soils[current_node, city]
                    weights.append(((T[city] + remj[city[0]] + remm[city[1]]) / Tsum) ** beta / (epsilon + s) ** alpha)
            else:
                for city in unfinished:
                    s = soils[current_node, city]
                    weights.append(HUD[city] / (epsilon + s) ** alpha)
            the_city = random.choices(unfinished, weights=weights)[0]
            unfinished.remove(the_city)
            path.append(the_city)
            if HEUR == 'ltrp':
                remj[the_city[0]] -= T[the_city]
                remm[the_city[1]] -= T[the_city]
            # local update: the drop deposits a bit of soil, so the next drops of this
            # iteration are nudged to other edges (diversification inside an iteration)
            s = soils[current_node, the_city]
            soils[current_node, the_city] = (1 - rhon) * s + rhon * soil_hi
            current_node = the_city
        iwdEnd = Time.time()

        MS, ST, FT = decode(path)
        makespanEnd = Time.time()
        iwdtimes.append(iwdEnd - iwdStart)
        makespantimes.append(makespanEnd - iwdEnd)

        if MS < MSIB: #update MSIB
            MSIB= MS
            IB= path
            STB= ST
            FTB= FT

    # local search on the iteration best
    lsStart = Time.time()
    budget = int(LS_BUDGET * N)
    if budget > 0:
        IB, MSIB, STB, FTB = local_search(IB, MSIB, STB, FTB, budget - int(TB_SHARE * budget))
    IB, MSIB, STB, FTB = canonical(IB, MSIB, STB, FTB)

    if MSIB< MSTB: #update MSTB
        MSTB= MSIB
        TB= list(IB)
        STT= STB
        FTT= FTB
        best= iterasi
        stag = 0
    else:
        stag += 1
    # intensification: keep polishing the total best with the rest of the budget
    if budget > 0 and int(TB_SHARE * budget) > 0:
        TB, MS2, ST2, FT2 = local_search(TB, MSTB, STT, FTT, int(TB_SHARE * budget))
        if MS2 < MSTB:
            MSTB, STT, FTT = MS2, ST2, FT2
            best = iterasi
            stag = 0
        TB, MSTB, STT, FTT = canonical(TB, MSTB, STT, FTT)
    lstimes.append(Time.time() - lsStart)

    # global update: evaporation (soil flows back towards initsoil everywhere) ...
    for key in soils:
        s = soils[key]
        soils[key] = s + rhoiwd * (soil_hi - s)
    # ... then erosion along the iteration-best and the total-best paths
    erode(IB, rhoiwd * (1 - tbweight))
    erode(TB, rhoiwd * tbweight)

    if stag >= stagmax:
        reset_soil()
        stag = 0
    print("iteration number {} done. MSIB: {}. Best: {}.".format(iterasi, MSIB, MSTB))

print("Start time best: {}".format(STT))
print("Finish time best: {}".format(FTT))
print("best iteration: {}".format(best))

print("MSTB: {}".format(MSTB))
print("TB: {}".format(TB))
endTime = Time.time()
print("time elapsed: {}".format(endTime - startTime))
print("iwd time max: {}".format(max(iwdtimes)))
print("makespan time max: {}".format(max(makespantimes)))
print("local search time max: {}".format(max(lstimes)))
