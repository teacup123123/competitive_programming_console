//
// Created by teacup123123 on 1/15/2021.
//

#ifndef STARTCF_PY_STRPROC_H
#define STARTCF_PY_STRPROC_H

list <string> split(string line, char splitby) {
    list <string> ans;
    ans.eb("");
    auto writing = ans.end();
    writing--;
    trav(c, line)
    {
        if (c == splitby) {
            ans.eb("");
            writing = ans.end();
            writing--;
            continue;
        } else
            *writing = *writing + c;
    }
    return ans;
}

#endif //STARTCF_PY_STRPROC_H
