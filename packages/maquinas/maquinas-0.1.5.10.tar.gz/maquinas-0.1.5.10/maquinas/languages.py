import types

class Language():
    def __init__(self,elements=[],max=30,finite=True,gen=None):
        """ Create a language 

        :param elements: This can be a finite enumeration of elements, another Language or a generator for an infinite language
        :param max: Maximum number of elements to print for infinite languages (default 30)
        :param finite: For languages based of generator if the language is finite or infinite, be aware theres is not check on this property and could raise errors (default True)"""
        self.max=max
        if isinstance(elements,Language):
            self.elements=elements.elements
            self.gen=elements.gen
            self.finite=elements.finite
        elif isinstance(gen,tuple):
            self.gen=gen
            self.elements=None
            self.finite=finite
        else:
            self.elements=set([str(e) for e in elements])
            self.gen=None
            self.finite=True

    def __iter__(self):
        if self.finite:
            for ele in self.elements:
                yield ele
        else:
            f,*args=self.gen
            yield from f(*args)

    def _epsilon(self,x):
        return 'ε' if len(x)==0 else str(x)

    def __repr__(self):
        if self.finite:
            return f"{{{','.join([self._epsilon(x) for x in self])}}}"
        else:
            return f"{{{','.join([self._epsilon(x) for _, x in zip(range(self.max), self)])},…}}"

    def __len__(self):
        if self.finite:
            return len(self.elements)
        else:
            return float('inf')

    def union(self,L):
        """ Union of the language with another language, if one is infintie returns an infinite generator

        :param L: Second Languauge fo the union
        :returns: Language  _self ∪ L_ """
        if self.finite and L.finite:
            return Language(self.elements.union(L),finite=True)
        else:
            return Language(gen=(self._union,L),finite=False)

    def _union(self,L):
        seen=set()
        for w in zip(self.elements,L):
            if not w in seen:
                seen.add(w)
                yield w
        for w in L:
            if not w in seen:
                seen.add(w)
                yield w

    def power(self,n):
        """ Power of a language 

        :returns: Language  _self^n_ """
        if n==0:
            return Language([""],finite=True)
        elif n==1:
            return Language(self)
        else:
            if self.finite:
                return Language(set(p for p in self._power(self,1,n)),finite=True)
            else:
                return Language(gen=(self._power,self,1,n),finite=False)

    def _power(self,partial,i,j):
        if i==j:
            for ele in partial:
                yield ele
        elif i<j:
            yield from self._power(self.concat(partial),i+1,j)


    def star(self):
        """ Star clouse for a language returns and infinite language 

        :returns: Language  _self*_ """
        return Language(gen=(self._star,),finite=False)

    def _star(self):
        yield ''
        prev=[""]
        seen=set([""])
        while True:
            for pre in prev:
                for ele in self:
                    new=pre+ele
                    if not new in seen:
                        prev.append(new)
                        seen.add(new)
                        yield new
            prev=[]

    def plus(self):
        """ Star clouse for a language returns an infinite language 

        :returns: Language  _self+_ """
        return Language(gen=(self._plus,),finite=False)

    def _plus(self):
        prev=[]
        seen=set()
        for e in self.elements:
            prev.append(e)
            yield  e
        while True:
            for pre in prev:
                for ele in self:
                    new=pre+ele
                    prev.append(new)
                    if not new in seen:
                        seen.add(new)
                        yield new
            prev=[]

    def concat(self,L):
        """ Concatenatio of the language with another language, if one is infintie returns an infinite generator

        :param L: Second Languauge fo the concatenation
        :returns: Language  _self L_ """
        if self.finite and L.finite:
            return Language([w1+w2 for w2 in L for w1 in self],finite=True)
        else:
            return Language(gen=(self._concat,L),finite=False)

    def _concat(self,L):
        seen=set()
        for w2 in L:
            for w1 in self:
                new=w1+w2
                if not new in seen:
                    seen.add(new)
                    yield w1+w2


class Alphabet(set):
    """ Wrapper for the set python class"""

    def star(self):
        """ Star clouse for an alphabet returns an infinite language 

        :returns: Language  _self*_ """
        return Language(gen=(self._star,),finite=False)

    def _star(self):
        seen=set()
        yield ''
        prev=[""]
        while True:
            for pre in prev:
                for ele in self:
                    new=pre+ele
                    prev.append(new)
                    if not new in seen:
                        seen.add(new)
                        yield new
            prev=[]

    def power(self,n):
        """ Power of an alphabet

        :returns: Language  _Σ^n_ """
        if n==0:
            return Language([""],finite=True)
        elif n==1:
            return Language(self)
        else:
            return Language(set(p for p in self._power(self,1,n)),finite=True)

    def _power(self,partial,i,j):
        if i==j:
            for ele in partial:
                yield ele
        elif i<j:
            yield from self._power(Language([w1+w2 for w2 in partial for w1 in self],finite=True)
,i+1,j)


