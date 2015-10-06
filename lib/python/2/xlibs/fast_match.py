# -*- coding:utf-8 -*-

def fast_match(pattern, text):
    nexts = compile(pattern)
    i = 0; cur = 0; maxcur = len(pattern) - 1
    while i < len(text):
        c = text[i]
        if c != pattern[cur]:
            if nexts[cur] == -1:
                i += 1
            else:
                cur = nexts[cur]
        else:
            if cur == maxcur:
                return i - cur
            else:
                cur += 1
                i += 1
    return -1


def compile(pattern):
    nexts = [-1,]; nextcur = 0
    for i in range(1, len(pattern)):
        matched_subst = pattern[:i]
        szsubst = len(matched_subst)
        # print 'matched_subst:', matched_subst
        # for j in range(1, len(matched_subst)):
        #     print matched_subst[:j]

        for j in range(1, len(matched_subst)):
            # print matched_subst[j:]
            if matched_subst.startswith(matched_subst[j:]):
                nextcur = szsubst - j; break
        nexts.append(nextcur)
    return nexts





if __name__ == '__main__':
    print compile('abcdabd')
    s = 'abahfsdabcdadsabcdabdsdafa'
    i = fast_match('abcdabd', s)
    print s[i:]


