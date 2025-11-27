module main

import os
import flag



fn main() {
    // define blacklisted letters
    blacklist := ["[", "]", "(", ")", "!", "§", "¡", "&"]

    // initialize flag(argument) parser
    mut fp := flag.new_flag_parser(os.args)

    
    // set version
    fp.application("resourcepackrenamer")
    fp.version("0.0.1")
    fp.description("rename my packs for me")

    // argument(s)
    path := fp.string("path", `p`, "none", "path for processing")

    // if user didn't provide a path; return
    if path == "none" {
        println("a file path is required.")
        return
    }
    // loop through all the files in the provided location
    for mut file in os.ls(path) or { [] } {
        oldfile := file
        // remove blacklisted stuffs
        for item in blacklist { file = file.replace(item, "") }
        os.mv("${path}/${oldfile}", "${path}/${file}")!
        println(oldfile + " -> " + file)
        
    }
}
