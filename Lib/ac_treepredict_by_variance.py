#Original code was retrieved from https://github.com/nico/collectiveintelligence-book

import collections
import numpy as np

class decisionnode(object):
#makoto.sano@prometric.com
#  def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, 
#      deviance=None, root_deviance=0.0, depth=-1, value_name=None):
  def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, 
      deviance=0.0, root_deviance=0.0, depth=-1, value_name=None):
    self.col = col  # colum index of value to test
    self.value = value  # reference value
    self.results = results  # stores results in leafs, empty for inner nodes
    self.tb = tb  # child on true branch
    self.fb = fb  # child on false branch
    self.deviance = deviance  # deviance of current node
    self.root_deviance = root_deviance  # deviance of root node
    self.depth = depth  # index of depth (number of recursive calls)
    self.value_name = value_name

def divideset(rows, column, value):
  split_function = None

  #numpy.int64 is not recognized as int. makoto.sano@prometric.com  
  if isinstance(value, int) or isinstance(value, float) or isinstance(value, np.integer):
    split_function = lambda row: row[column] >= value
  else:
    split_function = lambda row: row[column] == value
    
  # There has to be a `partition` or `group` function somewhere
  set1 = [row for row in rows if split_function(row)]
  set2 = [row for row in rows if not split_function(row)]
  return (set1, set2)


def uniquecounts(rows):
  results = collections.defaultdict(int)
  for row in rows:
    # Result is last column
    r = row[len(row) - 1]
    results[r] += 1
  return dict(results)


def giniimpurity(rows):
  """Returns probability that a randomly placed item will end up in the wrong
  category. A low result means that stuff is categorized well."""
  total = len(rows)
  counts = uniquecounts(rows)
  imp = 0
  # O(n^2) in number of categories
  for k1 in counts:
    p1 = float(counts[k1])/total  # XXX: These loops can be written more nicely
    for k2 in counts:
      if k1 == k2: continue
      p2 = float(counts[k2])/total
      imp += p1*p2
  return imp


def entropy(rows):
  from math import log
  log2 = lambda x: log(x)/log(2)
  results = uniquecounts(rows)
  ent = 0.0
  for r in results:
    p = float(results[r])/len(rows)
    ent -= p*log2(p)
  return ent


def variance(rows):
  if len(rows) == 0: return 0
  data = [float(row[len(row) - 1]) for row in rows]
  mean = sum(data) / len(data)

  # this gives indexoutofbounds in zillow example
  #variance = sum([(d-mean)**2 for d in data]) / (len(data) - 1)

  variance = sum([(d-mean)**2 for d in data]) / len(data)
  return variance


#makoto.sano@prometric.com
def getavrg_num(tree):
  num = 0
  avrg = 0.0  
  if tree.results != None:  # leaf node
    for key, val in tree.results.items():  #key is difficulty value, val is frequency
      avrg += (key * val)
      num += val
    avrg /= num      
    return avrg, num

  avrgt, numt = getavrg_num(tree.tb)
  avrgf, numf = getavrg_num(tree.fb)
  num = numt + numf
  avrg = ((avrgt * numt) + (avrgf * numf)) / num
  return avrg, num


#def buildtree(rows, scorefun=entropy): makoto.sano@prometric.com
def buildtree(rows, value_names=None, root_deviance=0.0, depth=0, scorefun=variance):
  if len(rows) == 0: return decisionnode()
  current_score = scorefun(rows)
  current_deviance = current_score * len(rows)

  if current_deviance >= root_deviance:
      root_deviance = current_deviance

  best_gain = 0.0
  best_criteria = None
  best_sets = None

  column_count = len(rows[0]) - 1  # last column is result
  for col in range(0, column_count):
    # find different values in this column
    column_values = set([row[col] for row in rows])

    # for each possible value, try to divide on that value
    for value in column_values:
      set1, set2 = divideset(rows, col, value)

      # Information gain
      # makoto.sano@prometric.com
      if scorefun == variance:
        gain = current_deviance - scorefun(set1)*len(set1) - scorefun(set2)*len(set2)
      else:
        p = float(len(set1)) / len(rows)
        gain = current_score - p*scorefun(set1) - (1-p)*scorefun(set2)

      if gain > best_gain and len(set1) > 0 and len(set2) > 0:
        best_gain = gain
        best_criteria = (col, value)
        best_sets = (set1, set2)
        print('%s %s %s %s %s %s %s %s' % ('Dept:', depth, ' Best Gain:', best_gain, ' Col:', col, 'Value:', value))

  if best_gain > 0:
    trueBranch = buildtree(best_sets[0], value_names, root_deviance, depth +1)
    falseBranch = buildtree(best_sets[1], value_names, root_deviance, depth +1)

    dn_value_name = ''

    if value_names != None:
      dn_value_name = value_names[best_criteria[0]]
    else:
      dn_value_name = None

    return decisionnode(col=best_criteria[0], value=best_criteria[1],
        tb=trueBranch, fb=falseBranch, deviance=current_deviance,
        root_deviance=root_deviance, depth=depth, value_name=dn_value_name)
  else:
    return decisionnode(results=uniquecounts(rows))

def printtree(tree, indent=''):
  #makoto.sano@prometric.com
  avrg, num = getavrg_num(tree)
  if tree.results != None:  # leaf
    print( '(Deviance:%1.4f, Depth:%s) Average:%1.4f, Count:%s ' % (tree.deviance, tree.depth, avrg, num) + ';'.join(['%s:%d' % v for v in tree.results.items()]))
  else:
    colname = ''
    if tree.value_name != None:
      colname = tree.value_name
    else:
      colname = str(tree.col)
    print('%s:%s? (Deviance:%1.4f, Depth:%s) Average:%1.4f, Count:%s' % (colname, tree.value, tree.deviance, tree.depth, avrg, num))
    print(indent + 'T-> ', end="")
    printtree(tree.tb, indent + '  ')
    print(indent + 'F-> ', end="")
    printtree(tree.fb, indent + '  ')


def classify(observation, tree):
  if tree.results != None:  # leaf
    #makoto.sano@prometric.com
    #return tree.results
    return getavrg_num(tree)
  else:
    v = observation[tree.col]
    branch = None
    if isinstance(v, int) or isinstance(v, float):
      if v >= tree.value: branch = tree.tb
      else: branch = tree.fb
    else:
      if v == tree.value: branch = tree.tb
      else: branch = tree.fb
    return classify(observation, branch)


#def prune(tree, mingain): makoto.sano@prometric.com
def prune(tree, mingain, scorefun=variance):
  # recurse
  if tree.tb.results == None: prune(tree.tb, mingain)
  if tree.fb.results == None: prune(tree.fb, mingain)

  # merge leaves (potentionally)
  if tree.tb.results != None and tree.fb.results != None:
    tb, fb = [], []
    #for v, c in tree.tb.results.iteritems(): tb += [[v]] * c
    #for v, c in tree.fb.results.iteritems(): fb += [[v]] * c
    for v, c in tree.tb.results.items(): tb += [[v]] * c
    for v, c in tree.fb.results.items(): fb += [[v]] * c

    # makoto.sano@prometric.com
    if scorefun == variance:
      delta = scorefun(tb+fb)*(len(tb+fb)) - scorefun(tb)*len(tb) - scorefun(fb)*len(fb)
    else:
      p = float(len(tb)) / len(tb + fb)
      delta = entropy(tb+fb) - p*entropy(tb) - (1-p)*entropy(fb)

    if delta < mingain:
      tree.tb, tree.fb = None, None
      tree.results = uniquecounts(tb + fb)


# 'missing data classify'
def mdclassify(observation, tree):
  if tree.results != None:  # leaf
    return tree.results
  else:
    v = observation[tree.col]
    if v == None:
      tr = mdclassify(observation, tree.tb)
      fr = mdclassify(observation, tree.fb)
      tcount = sum(tr.values())
      fcount = sum(fr.values())
      tw = float(tcount)/(tcount + fcount)
      fw = float(fcount)/(tcount + fcount)
      result = collections.defaultdict(int)
      #for k, v in tr.iteritems(): result[k] += v*tw
      #for k, v in fr.iteritems(): result[k] += v*fw
      for k, v in tr.items(): result[k] += v*tw
      for k, v in fr.items(): result[k] += v*fw
      return dict(result)
    else:
      branch = None
      if isinstance(v, int) or isinstance(v, float):
        if v >= tree.value: branch = tree.tb
        else: branch = tree.fb
      else:
        if v == tree.value: branch = tree.tb
        else: branch = tree.fb
      return classify(observation, branch)


#makoto.sano@prometric.com
def deviance_by_recursive_call(tree, deviance_dic):
  if tree.depth != -1:
    if tree.depth in deviance_dic:
      deviance_dic[tree.depth] = deviance_dic[tree.depth] + tree.deviance
    else:
      deviance_dic[tree.depth] = tree.deviance
  if tree.results != None: # pruned leaf
    if (-1 * tree.depth) in deviance_dic:
      deviance_dic[(-1 * tree.depth)] = deviance_dic[(-1 * tree.depth)] + tree.deviance
    else:
      deviance_dic[(-1 * tree.depth)] = tree.deviance
  else:
    deviance_by_recursive_call(tree.tb, deviance_dic)
    deviance_by_recursive_call(tree.fb, deviance_dic)


#makoto.sano@prometric.com
def finalize_deviance(deviance_dic):
  for key, val in sorted(deviance_dic.items()):
    if key < 0:
      num = (-1 * key) + 1
      while num < len(deviance_dic):
        if num in deviance_dic:
          deviance_dic[num] = deviance_dic[num] + deviance_dic[key]
        num += 1


#makoto.sano@prometric.com
def print_r2_by_recursive_call(tree, deviance_dic):
  for key, val in sorted(deviance_dic.items()):
    if key >= 0: # Hide internal R2 for pruned leaf
      print('%s %s %s %1.4f' % ('R2 after', key, 'recursive call(s):', 1- val/tree.root_deviance))


#makoto.sano@prometric.com
def data_for_treebuild(df_ac_data, data_for_tree_columns, res_column):
  df_ac_data_for_tree = df_ac_data.loc[:,data_for_tree_columns]
  df_ac_data_for_tree[res_column] = df_ac_data[res_column]

  ac_buf_index = df_ac_data_for_tree.index
  ac_buf_columns = list(df_ac_data_for_tree.columns)

  tree_data = []

  for i, index_value in enumerate(ac_buf_index):
      tree_data.append(list(df_ac_data_for_tree.iloc[i]))

  return (tree_data, ac_buf_columns)
