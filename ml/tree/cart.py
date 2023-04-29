# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/601_tree.cart.ipynb.

# %% auto 0
__all__ = ['TreeNode', 'sqsplit_helper', 'sqsplit', 'cart_helper', 'cart', 'eval_helper', 'eval_tree', 'forest', 'eval_forest']

# %% ../../nbs/601_tree.cart.ipynb 5
class TreeNode(object):
    """Tree class.
    """
    
    def __init__(self, left, right, parent, cutoff_id, cutoff_val, prediction):
        self.left = left
        self.right = right
        self.parent = parent
        self.cutoff_id = cutoff_id
        self.cutoff_val = cutoff_val
        self.prediction = prediction
        
        

# %% ../../nbs/601_tree.cart.ipynb 9
def sqsplit_helper(xTr, yTr, weights, dim):
    """ Finds the best cut value and loss value for feature d
    
    Input:
        xTr:     n x d matrix of data points
        yTr:     n-dimensional vector of labels
        weights: n-dimensional weight vector for data points
        dim:     dimension to consider
    
    Output:
        cut:      cut-value of the best cut
        bestloss: loss of the best cut
    """
    N, _ = xTr.shape
    f, y, w = xTr[:,dim], yTr, weights
    ind = np.argsort(f)
    f, y, w = f[ind], y[ind], w[ind]
    
    cut = np.inf
    bestloss = np.inf
    
    WL = 0.0
    WR = 1.0
    PL = 0.0
    PR = np.inner(w, y)
    QL = 0.0
    QR = np.inner(w, y**2)
    
    for i in range(N-1):
        WL += w[i]
        WR -= w[i]
        PL += w[i] * y[i]
        PR -= w[i] * y[i]
        QL += w[i] * y[i]**2
        QR -= w[i] * y[i]**2
        leftL = QL - PL * PL / WL
        rightL = QR - PR * PR / WR
        loss = leftL + rightL
        if f[i] != f[i+1] and loss < bestloss:
            bestloss = loss
            cut = (f[i] + f[i+1]) / 2
            
    return cut, bestloss
    

def sqsplit(xTr,yTr,weights=None):
    """Finds the best feature, cut value, and loss value.
    
    Input:
        xTr:     n x d matrix of data points
        yTr:     n-dimensional vector of labels
        weights: n-dimensional weight vector for data points
    
    Output:
        feature:  index of the best cut's feature
        cut:      cut-value of the best cut
        bestloss: loss of the best cut
    """
    N,D = xTr.shape
    assert D > 0 # must have at least one dimension
    assert N > 1, xTr# must have at least two samples
    if weights is None: # if no weights are passed on, assign uniform weights
        weights = np.ones(N)
    weights = weights/sum(weights) # Weights need to sum to one (we just normalize them)
    bestloss = np.inf
    feature = np.inf
    cut = np.inf
    
    for dim in range(D):
        c, loss = sqsplit_helper(xTr, yTr, weights, dim)
        if loss < bestloss:
            cut = c
            bestloss = loss
            feature = dim
    
    return feature, cut, bestloss

# %% ../../nbs/601_tree.cart.ipynb 12
def cart_helper(xTr, yTr, depth, weights, maxDepth):
    if xTr.shape[0] == 1:
        return TreeNode(None, None, None, None, None, yTr[0])

    w = weights / np.sum(weights)
    pred = np.dot(yTr, w)
    
    if depth == maxDepth or \
        np.var(yTr) == 0:
        # this is too expensive, better let sqsplit step
        # np.sum(np.var(xTr, axis=0)) == 0:
        return TreeNode(None, None, None, None, None, pred) # leaf
    
    feature, cut, loss = sqsplit(xTr, yTr, weights)
    
    leftIdx = np.where(xTr[:,feature] <= cut)
    rightIdx = np.where(xTr[:,feature] > cut)
    
    if len(leftIdx[0]) == 0 or len(rightIdx[0]) == 0: # 
        return TreeNode(None, None, None, None, None, pred)

    leftR = cart_helper(xTr[leftIdx], yTr[leftIdx], depth+1, weights[leftIdx], maxDepth)
    rightR = cart_helper(xTr[rightIdx], yTr[rightIdx], depth+1, weights[rightIdx], maxDepth)
    
    root = TreeNode(leftR, rightR, None, feature, cut, pred)
    leftR.parent = root
    rightR.parent = root
    
    return root
    
    
def cart(xTr,yTr,maxdepth=np.inf,weights=None):
    """Builds a CART tree.
    
    The maximum tree depth is defined by "maxdepth" (maxdepth=2 means one split).
    Each example can be weighted with "weights".

    Args:
        xTr:      n x d matrix of data
        yTr:      n-dimensional vector
        maxdepth: maximum tree depth
        weights:  n-dimensional weight vector for data points

    Returns:
        tree: root of decision tree
    """
    n, _ = xTr.shape
    if weights is None:
        w = np.ones(n) / float(n)
    else:
        w = weights
    
    if n == 0:
        return None
    return cart_helper(xTr, yTr, 1, w, maxdepth)

# %% ../../nbs/601_tree.cart.ipynb 13
def eval_helper(root, point):
    if root.left is None and root.right is None: # is leaf
        return root.prediction
    
    dim = root.cutoff_id
    if point[dim] <= root.cutoff_val:
        return eval_helper(root.left, point)
    else:
        return eval_helper(root.right, point)

    
def eval_tree(root,xTe):
    """Evaluates xTe using decision tree root.
    
    Input:
        root: TreeNode decision tree
        xTe:  n x d matrix of data points
    
    Output:
        pred: n-dimensional vector of predictions
    """
    assert root is not None
    n = xTe.shape[0]
    pred = np.zeros(n)
    
    for i, x in enumerate(xTe):
        pred[i] = eval_helper(root, x)

    return pred

# %% ../../nbs/601_tree.cart.ipynb 21
def forest(xTr, yTr, m, maxdepth=np.inf):
    """Creates a random forest.
    
    Input:
        xTr:      n x d matrix of data points
        yTr:      n-dimensional vector of labels
        m:        number of trees in the forest
        maxdepth: maximum depth of tree
        
    Output:
        trees: list of TreeNode decision trees of length m
    """
    
    n, d = xTr.shape
    trees = []
    
    for _ in range(m):
        idx = np.random.choice(n, n)
        x = xTr[idx]
        y = yTr[idx]
        node = cart(x, y, maxdepth)
        trees.append(node)
    
    return trees

# %% ../../nbs/601_tree.cart.ipynb 22
def eval_forest(trees, X, alphas=None):
    """Evaluates X using trees.
    
    Input:
        trees:  list of TreeNode decision trees of length m
        X:      n x d matrix of data points
        alphas: m-dimensional weight vector
        
    Output:
        pred: n-dimensional vector of predictions
    """
    m = len(trees)
    n,d = X.shape
    if alphas is None:
        alphas = np.ones(m) / len(trees)            
    pred = np.zeros(n)
    
    cont = []
    for tree in trees:
        cont.append(eval_tree(tree, X))
    pred = alphas.dot(cont)
    
    return pred
