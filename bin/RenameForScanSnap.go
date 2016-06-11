// 
// ScanSnapでソート順を守るようにリネームする
// 
// RenameForScanSnap <ディレクトリ>
//
// ex)
// 20151031155010.jpg    -> 20151031155010000.jpg
// 20151031155010000.jpg -> 20151031155010001.jpg
// 
package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
)

// ByFileNameList : ソート用の型
type ByFileNameList []os.FileInfo

func (list ByFileNameList) Len() int {
	return len(list)
}
func (list ByFileNameList) Swap(i, j int) {
	list[i], list[j] = list[j], list[i]
}
func (list ByFileNameList) Less(i, j int) bool {
	return list[i].Name() < list[j].Name()
}

func main() {

	dirName := os.Args[1]

	fileInfoList, err := ioutil.ReadDir(dirName)
	if err != nil {
		panic(err)
	}
	// 逆順ソートする
	var list ByFileNameList
	list = fileInfoList
	sort.Sort(sort.Reverse(list))

	for _, f := range list {
		fname := f.Name()
		var nname string

		if f.IsDir() {
			continue
		}

		if len(fname) == 21 {
			nname = fname[:14] + "001.jpeg"

		} else if len(fname) == 18 {
			nname = fname[:14] + "000.jpeg"
		} else {
			continue
		}

		fmt.Println(dirName + "/" + fname)
		fmt.Println(dirName + "/" + nname)
		// ファイル移動
		os.Rename(dirName+"/"+fname, dirName+"/"+nname)

	}
}
