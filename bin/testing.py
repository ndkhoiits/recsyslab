def slopeone():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.split(r.getR(), 12320894329854567890)

    from recommender import slopeone
    so = slopeone.slopeone(train)

    # import cPickle
    # output = open("slopeone.npz", "wb")
    # cPickle.dump(so, output, -1)
    # output.close()

    # inputfile = open("slopeone.npz", "rb")
    # so = cPickle.load(inputfile)
    # inputfile.close()

    from util import test
    test.auc(test1, so.getRec, r)

# slopeone()


def svd():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import svd
    W, H = svd.learnModel(r.getMaxUid(), r.getMaxIid(),
                          0.0002, train, 1000, 25, r.numberOfTransactions)
    import numpy as np
    np.savez_compressed(
        "SVDModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    from util import test
    t = test.MFtest(W, H, train)
    test.hitrate(test1, t.getRec, 10)

# svd()


def mf():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import mf
    W, H = mf.learnModel(r.getMaxUid(), r.getMaxIid(), 0.01, 0.01, 0.01,
                         0.1, train, 150, 3, r.numberOfTransactions,
                         mf.logLoss, mf.dLogLoss)
    import numpy as np
    # np.savez_compressed(
    #    "BPRMFModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    from util import test
    t = test.MFtest(W, H, train)
    test.hitrate(test1, t.getRec, 10)

# mf()


def knn():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.splitMatrix(r.getMatrix(), 1234567890)

    from recommender import knn
    k = knn.itemKnn(train, 10)

    from util import test
    print test.auc(test1, k.getRec, r)

# knn()


def simple():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import primitive
    c = primitive.randomRec(r.getR())

    from util import test
    test.auc(test1, c.getRec, r)

# simple()
