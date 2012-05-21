$fileOriginalCopy = "fogbugz.py.origCopy"
$file = "fogbugz.py"
copy $file $fileOriginalCopy

(cat $file) | 
  foreach{$_.replace("from BeautifulSoup import BeautifulSoup, CData", "from BeautifulSoup.BeautifulSoup import BeautifulSoup, CData")} | 
  out-file fogbugz.py -encoding "ASCII"
  
python setupWindowsBuild.py bdist_wininst --plat-name=win32

copy $fileOriginalCopy $file
del $fileOriginalCopy