# -*- coding: utf-8 -*-
r"""
Mutually Orthogonal Latin Squares (MOLS)

A Latin square is an `n\times n` array filled with `n` different symbols, each
occurring exactly once in each row and exactly once in each column. For Sage's
methods related to Latin Squares, see the module
:mod:`sage.combinat.matrices.latin`.

This module gathers constructions of Mutually Orthogonal Latin Squares, which
are equivalent to Transversal Designs and specific Orthogonal Arrays.

For more information on MOLS, see the :wikipedia:`Wikipedia entry on MOLS
<Graeco-Latin_square#Mutually_orthogonal_Latin_squares>`.

TODO:

* Implement Wilson's construction (page 146 of [Stinson2004]_)
* Look at [ColDin01]_.

REFERENCES:

.. [Stinson2004] Douglas R. Stinson,
  Combinatorial designs: construction and analysis,
  Springer, 2004.

.. [ColDin01] Charles Colbourn, Jeffrey Dinitz,
  Mutually orthogonal latin squares: a brief survey of constructions,
  Volume 95, Issues 1-2, Pages 9-48,
  Journal of Statistical Planning and Inference,
  Springer, 1 May 2001.
"""

def are_mutually_orthogonal_latin_squares(l, verbose=False):
    r"""
    Check wether the list of matrices in ``l`` form mutually orthogonal latin
    squares.

    INPUT:

    - ``verbose`` - if ``True`` then print why the list of matrices provided are
      not mutually orthogonal latin squares

    EXAMPLES::

        sage: from sage.combinat.designs.latin_squares import are_mutually_orthogonal_latin_squares
        sage: m1 = matrix([[0,1,2],[2,0,1],[1,2,0]])
        sage: m2 = matrix([[0,1,2],[1,2,0],[2,0,1]])
        sage: m3 = matrix([[0,1,2],[2,0,1],[1,2,0]])
        sage: are_mutually_orthogonal_latin_squares([m1,m2])
        True
        sage: are_mutually_orthogonal_latin_squares([m1,m3])
        False
        sage: are_mutually_orthogonal_latin_squares([m2,m3])
        True
        sage: are_mutually_orthogonal_latin_squares([m1,m2,m3], verbose=True)
        matrices 0 and 2 are not orthogonal
        False

        sage: m = designs.mutually_orthogonal_latin_squares(8,7)
        sage: are_mutually_orthogonal_latin_squares(m)
        True
    """
    if not l:
        raise ValueError("the list must be non empty")

    n = l[0].nrows()
    if any(M.nrows() != n and M.ncols() != n for M in l):
        if verbose:
            print "some matrix has wrong dimension"
        return False

    # check that the matrices in l are actually latin
    for i,M in enumerate(l):
        if (any(sorted(r) != range(n) for r in M.rows()) or
            any(sorted(c) != range(n) for c in M.columns())):
            if verbose:
                print "matrix %d is not latin"%i
            return False

    # check orthogonality of each pair
    for k1 in xrange(len(l)):
        M1 = l[k1]
        for k2 in xrange(k1):
            M2 = l[k2]
            L = [(M1[i,j],M2[i,j]) for i in xrange(n) for j in xrange(n)]
            if len(set(L)) != len(L):
                if verbose:
                    print "matrices %d and %d are not orthogonal"%(k2,k1)
                return False

    return True

def mutually_orthogonal_latin_squares(n,k, partitions = False, check = True, availability=False, who_asked=tuple()):
    r"""
    Returns `k` Mutually Orthogonal `n\times n` Latin Squares (MOLS).

    For more information on Latin Squares and MOLS, see
    :mod:`~sage.combinat.designs.latin_squares` or the :wikipedia:`Latin_square`,
    or even the
    :wikipedia:`Wikipedia entry on MOLS <Graeco-Latin_square#Mutually_orthogonal_Latin_squares>`.

    INPUT:

    - ``n`` (integer) -- size of the latin square.

    - ``k`` (integer) -- number of MOLS.

    - ``partition`` (boolean) -- a Latin Square can be seen as 3 partitions of
      the `n^2` cells of the array into `n` sets of size `n`, respectively :

      * The partition of rows
      * The partition of columns
      * The partition of number (cells numbered with 0, cells numbered with 1,
        ...)

      These partitions have the additional property that any two sets from
      different partitions intersect on exactly one element.

      When ``partition`` is set to ``True``, this function returns a list of `k+2`
      partitions satisfying this intersection property instead of the `k+2` MOLS
      (though the data is exactly the same in both cases).

    - ``availability`` (boolean) -- if ``availability`` is set to ``True``, the
      function only returns boolean answers according to whether Sage knows how
      to build such a collection. This should be much faster than actually
      building it.

    - ``check`` -- (boolean) Whether to check that output is correct before
      returning it. As this is expected to be useless (but we are cautious
      guys), you may want to disable it whenever you want speed. Set to
      ``True`` by default.

    - ``who_asked`` (internal use only) -- because of the equivalence between
      OA/TD/MOLS, each of the three constructors calls the others. We must keep
      track of who calls who in order to avoid infinite loops. ``who_asked`` is
      the tuple of the other functions that were called before this one.

    EXAMPLES::

        sage: designs.mutually_orthogonal_latin_squares(5,4)
        [
        [0 1 2 3 4]  [0 1 2 3 4]  [0 1 2 3 4]  [0 1 2 3 4]
        [3 0 1 4 2]  [4 3 0 2 1]  [1 2 4 0 3]  [2 4 3 1 0]
        [4 3 0 2 1]  [1 2 4 0 3]  [2 4 3 1 0]  [3 0 1 4 2]
        [1 2 4 0 3]  [2 4 3 1 0]  [3 0 1 4 2]  [4 3 0 2 1]
        [2 4 3 1 0], [3 0 1 4 2], [4 3 0 2 1], [1 2 4 0 3]
        ]
        sage: designs.mutually_orthogonal_latin_squares(7,3)
        [
        [0 1 2 3 4 5 6]  [0 1 2 3 4 5 6]  [0 1 2 3 4 5 6]
        [4 0 3 1 6 2 5]  [5 6 0 4 2 1 3]  [6 4 1 0 5 3 2]
        [5 6 0 4 2 1 3]  [6 4 1 0 5 3 2]  [1 3 5 2 0 6 4]
        [6 4 1 0 5 3 2]  [1 3 5 2 0 6 4]  [2 5 4 6 3 0 1]
        [1 3 5 2 0 6 4]  [2 5 4 6 3 0 1]  [3 2 6 5 1 4 0]
        [2 5 4 6 3 0 1]  [3 2 6 5 1 4 0]  [4 0 3 1 6 2 5]
        [3 2 6 5 1 4 0], [4 0 3 1 6 2 5], [5 6 0 4 2 1 3]
        ]
        sage: designs.mutually_orthogonal_latin_squares(5,2,partitions=True)
        [[[0, 1, 2, 3, 4],
          [5, 6, 7, 8, 9],
          [10, 11, 12, 13, 14],
          [15, 16, 17, 18, 19],
          [20, 21, 22, 23, 24]],
         [[0, 5, 10, 15, 20],
          [1, 6, 11, 16, 21],
          [2, 7, 12, 17, 22],
          [3, 8, 13, 18, 23],
          [4, 9, 14, 19, 24]],
        [[0, 6, 12, 18, 24],
          [1, 7, 14, 15, 23],
          [2, 9, 13, 16, 20],
          [3, 5, 11, 19, 22],
          [4, 8, 10, 17, 21]],
        [[0, 7, 13, 19, 21],
          [1, 9, 10, 18, 22],
          [2, 8, 11, 15, 24],
          [3, 6, 14, 17, 20],
          [4, 5, 12, 16, 23]]]

    TESTS::

        sage: designs.mutually_orthogonal_latin_squares(5,5)
        Traceback (most recent call last):
        ...
        ValueError: There exist at most n-1 MOLS of size n.
        sage: designs.mutually_orthogonal_latin_squares(6,3,availability=True)
        False
        sage: designs.mutually_orthogonal_latin_squares(10,2,availability=True)
        True
        sage: designs.mutually_orthogonal_latin_squares(10,2)
        [
        [1 8 9 0 2 4 6 3 5 7]  [1 7 6 5 0 9 8 2 3 4]
        [7 2 8 9 0 3 5 4 6 1]  [8 2 1 7 6 0 9 3 4 5]
        [6 1 3 8 9 0 4 5 7 2]  [9 8 3 2 1 7 0 4 5 6]
        [5 7 2 4 8 9 0 6 1 3]  [0 9 8 4 3 2 1 5 6 7]
        [0 6 1 3 5 8 9 7 2 4]  [2 0 9 8 5 4 3 6 7 1]
        [9 0 7 2 4 6 8 1 3 5]  [4 3 0 9 8 6 5 7 1 2]
        [8 9 0 1 3 5 7 2 4 6]  [6 5 4 0 9 8 7 1 2 3]
        [2 3 4 5 6 7 1 8 9 0]  [3 4 5 6 7 1 2 8 0 9]
        [3 4 5 6 7 1 2 0 8 9]  [5 6 7 1 2 3 4 0 9 8]
        [4 5 6 7 1 2 3 9 0 8], [7 1 2 3 4 5 6 9 8 0]
        ]

    """
    from sage.rings.finite_rings.constructor import FiniteField
    from sage.combinat.designs.block_design import AffineGeometryDesign
    from sage.combinat.designs.orthogonal_arrays import orthogonal_array
    from sage.rings.arith import is_prime_power
    from sage.matrix.constructor import Matrix
    from sage.rings.arith import factor

    if k >= n:
        if availability:
            return False
        else:
            raise ValueError("There exist at most n-1 MOLS of size n.")

    elif n == 10 and k == 2:
        if availability:
            return True

        from database import MOLS_10_2
        matrices = MOLS_10_2()

    elif is_prime_power(n):
        if availability:
            return True

        # Section 6.4.1 of [Stinson2004]
        Fp = FiniteField(n,'x')
        B = AffineGeometryDesign(2,1,Fp).blocks()
        parallel_classes = [[] for _ in range(k+2)]
        for b in B:
            for p in parallel_classes:
                if (not p) or all(i not in p[0] for i in b):
                    p.append(b)
                    break

        coord = {v:i
                 for i,L in enumerate(parallel_classes[0]) for v in L}
        coord = {v:(coord[v],i)
                 for i,L in enumerate(parallel_classes[1]) for v in L}

        matrices = []
        for P in parallel_classes[2:]:
            matrices.append(Matrix({coord[v]:i for i,L in enumerate(P) for v in L }))

        if partitions:
            partitions = parallel_classes

    elif (orthogonal_array not in who_asked and
        orthogonal_array(k+2,n,availability=True,who_asked = who_asked+(mutually_orthogonal_latin_squares,))):
        if availability:
            return True
        OA = orthogonal_array(k+2,n,check=False, who_asked = who_asked+(mutually_orthogonal_latin_squares,))
        OA.sort() # make sure that the first two columns are "11, 12, ..., 1n, 21, 22, ..."

        # We first define matrices as lists of n^2 values
        matrices = [[] for _ in range(k)]
        for L in OA:
            for i in range(2,k+2):
                matrices[i-2].append(L[i])

        # The real matrices
        matrices = [[M[i*n:(i+1)*n] for i in range(n)] for M in matrices]
        matrices = [Matrix(M) for M in matrices]

    else:
        if availability:
            return False
        else:
            raise NotImplementedError("I don't know how to build these MOLS!")

    if check:
        assert are_mutually_orthogonal_latin_squares(matrices)

    # partitions have been requested but have not been computed yet
    if partitions is True:
        partitions = [[[i*n+j for j in range(n)] for i in range(n)],
                      [[j*n+i for j in range(n)] for i in range(n)]]
        for m in matrices:
            partition = [[] for i in range(n)]
            for i in range(n):
                for j in range(n):
                    partition[m[i,j]].append(i*n+j)
            partitions.append(partition)

    if partitions:
        return partitions
    else:
        return matrices

def latin_square_product(M,N,*others):
    r"""
    Returns the product of two (or more) latin squares.

    Given two Latin Squares `M,N` of respective sizes `m,n`, the direct product
    `M\times N` of size `mn` is defined by `(M\times
    N)((i_1,i_2),(j_1,j_2))=(M(i_1,j_1),N(i_2,j_2))` where `i_1,j_1\in [m],
    i_2,j_2\in [n]`

    Each pair of values `(i,j)\in [m]\times [n]` is then relabeled to `in+j`.

    This is Lemma 6.25 of [Stinson2004]_.

    INPUT:

    An arbitrary number of latin squares (greater than 2).

    EXAMPLES::

        sage: from sage.combinat.designs.latin_squares import latin_square_product
        sage: m=designs.mutually_orthogonal_latin_squares(4,3)[0]
        sage: latin_square_product(m,m,m)
        64 x 64 sparse matrix over Integer Ring
    """
    from sage.matrix.constructor import Matrix
    m = M.nrows()
    n = N.nrows()

    D = {((i,j),(ii,jj)):(M[i,ii],N[j,jj])
         for i in range(m)
         for ii in range(m)
         for j in range(n)
         for jj in range(n)}

    L = lambda i_j: i_j[0] * n + i_j[1]
    D = {(L(c[0]),L(c[1])): L(v) for c,v in D.iteritems()}
    P = Matrix(D)

    if others:
        return latin_square_product(P, others[0],*others[1:])
    else:
        return P
