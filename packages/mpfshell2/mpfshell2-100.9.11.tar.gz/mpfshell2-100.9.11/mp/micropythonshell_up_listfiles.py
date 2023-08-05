import uos
import ubinascii
import uhashlib

def up_listfiles():
  def sha256(filename):
    JUNK = 256
    sha = uhashlib.sha256()
    with open(filename, 'rb') as f:
      while True:
        data = f.read(JUNK)
        if len(data) == 0:
          return ubinascii.hexlify(sha.digest())
        sha.update(data)

  f = []
  for filetuple in uos.ilistdir():
    filename = filetuple[0]
    filetype = filetuple[1]
    if filetype != 0x8000:
      # Not a file
      continue
    f.append((filename, sha256(filename)))
  return f
