module main

import os
import flag



fn main() {

    blacklist := ["[", "]", "(", ")", "!", "§", "¡", "&"]

    mut fp := flag.new_flag_parser(os.args)

    fp.application("resourcepackrenamer")
    fp.version("0.0.1")
    fp.description("rename my packs for me")

    path := fp.string("path", `p`, "none", "path for processing")


    if path == "none" {
        println("a file path is required.")
        return
    }

    for mut file in os.ls(path) or { [] } {
        oldfile := file
        // remove blacklisted stuffs
        for item in blacklist { file = file.replace(item, "") }
        os.mv("${path}/${oldfile}", "${path}/${file}")!
        println(oldfile + " -> " + file)
        
    }
}
