import os, requests

def make_formula(formula, file="output.png", negate=False):
    r = requests.get(r"https://latex.codecogs.com/png.image?\large&space;\dpi{300}\bg{white}%s" % formula)
    
    with open(file, "wb") as f:
        f.write(r.content)

    if negate:
        os.system(f"convert tmp.png -channel RGB -negate -colorspace rgb {file}")

    return file