module main

import os
import flag

fn main() {
    // define blacklisted letters
    mut blacklist := ["[", "]", "(", ")", "!", "§", "¡", "&"]   

    // initialize flag(argument) parser
    mut fp := flag.new_flag_parser(os.args)

    
    // set version(s)
    fp.application("resourcepackrenamer")
    fp.version("0.0.1")
    fp.description("rename my packs for me")

    // argument(s)
    path := fp.string("path", `p`, "none", "path for processing")

    help := fp.bool("help", `h`, false, "help")

    if help {
        info := {
            "--help, -h": "display this",
            "--path, -p": "set path(required)",
            "--override, -o": "override list of chars"
        }
        for key, val in info {
            println("${key}  <->  ${val}")
        }
        return
    }
    override := fp.string("override", `o`, "none", "override")

    // if user didn't provide a path; return
    if path == "none" {
        println("a file path is required.")
        println("--help for help")
        return
    }
    // override, overrides the blacklist with a string provided by the user
    if override != "none" {
        blacklist = override.split("")
    }
    // loop through all the files in the provided location
    for mut file in os.ls(path) or { [] } {

        oldfile := file
        // loop through the blacklisted chars
        for item in blacklist {

            // remove char
            file = file.replace(item, "")
        }
        // check if they are equal, so we don't waste no memory
        if oldfile != file {

            // rename(move) the old file
            os.mv("${path}/${oldfile}", "${path}/${file}")!

            // print information
            println(oldfile + " -> " + file)

        } else {
            println("nothing to do")
        }

        
    }
}
