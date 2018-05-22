'''
Created on 22/05/2018

@author: ernesto
'''
# XXX: https://practice.geeksforgeeks.org/problems/trie-delete/1
# XXX: 

'''
The story thus far... an engineer was just getting started implementing a trie. They got distracted and never finished. Implement the remove and lookup methods. Make sure the methods conform to the given docstrings. Feel free to change the existing implementation (including tests!) in any way. Use any resources you can think of, including Google/Wikipedia/Stack Overflow etc.


root
  \
   b
    \
    a
   / \
  r   l
       \
        l

'''
from string import ascii_lowercase

# trie.py
class Trie:

    def __init__(self):
        self.root = TrieNode('')
        self.children = {}
        self.is_word=False
    
    def add(self, word):
        '''
        Add a word to the trie
        '''
        boolean = False
        node = self.root
        iter_list = [x for x in range(len(word))]
        for i in iter_list:
            if 1 == len(word) - i:
                boolean = True
            letter = word[i]
            if letter in node.children:
                node = node.children[letter]             
                if boolean:
                    node.is_word = True
            else:
                new_node = TrieNode(letter)
                new_node.is_word = boolean
                node.children[letter] = new_node
                node = new_node
    
    def remove(self, word):
        '''
        Given a word, remove it from the trie
        such that it won't be returned from a lookup of its prefix
        If the word is not in the trie, do nothing.
        '''
        s=[]
        cn=self.root
        for c in word:
            if c not in cn.children:
                return
            nn=cn.children[c]
            s.append((cn,c))
            cn=nn
        cn.is_word=False
        while s:
            cn,c=s.pop()
            nn=cn.children[c]
            if nn.is_word or nn.children:
                return
            del cn.children[c]
            

    def getNodeWords(self, node, prefix):
        resp = []
        # nprefix = prefix + node.letter
        if node.is_word:
            resp.append(prefix)
        
#        for letter in node.children.keys():
        for letter in ascii_lowercase:
            if letter not in node.children:
                continue
            n = node.children[letter]
            r = self.getNodeWords(n, prefix + n.letter)
            if r:
                resp+= r
                    
        return resp
    
    def lookup(self, prefix):
        '''
        Given a prefix, return a list of words in the trie that match that prefix.
        The returned list is lexicographically sorted.
        '''
        node = self.root

        for letter in prefix:
            if letter in node.children:
                node = node.children[letter]
            else:
                return []
        
        return sorted(self.getNodeWords(node, prefix))
            
    
class TrieNode:

    def __init__(self, letter):
        self.letter = letter
        self.is_word = False
        self.children = {}

        
# test_trie.py
def test_trie_add():
    trie = Trie()
    trie.add('foo')
    trie.add('bar')
    trie.add('baz')
    assert len(trie.root.children) == 2
    assert len(trie.root.children['b'].children) == 1
    assert trie.root.children['b'].children['a'].children['r'].is_word
    assert trie.root.children['b'].children['a'].children['z'].is_word
    assert trie.root.children['f'].children['o'].children['o'].is_word


def test_trie_lookup():
    trie = Trie()
    trie.add('bar')
    trie.add('baz')
    trie.add('ba')
    trie.add('baaaz')
    assert trie.lookup('ba') == ['ba', 'baaaz', 'bar', 'baz']
    assert trie.lookup('baar') == []


def test_trie_remove():
    trie = Trie()
    trie.add('bar')
    trie.add('baz')
    trie.add('bart')
    trie.add('bast')
    trie.add('basm')
    assert trie.lookup('bar') == ["bar","bart"]
    trie.remove("bar")
    assert trie.lookup('bar') == ["bart"]
    assert trie.lookup('bas') == ["basm","bast"]
    trie.remove("bast")
    assert trie.lookup('bas') == ["basm"]

if __name__ == '__main__':
    test_trie_add()
    test_trie_lookup()
    test_trie_remove()
    print('Success!')
