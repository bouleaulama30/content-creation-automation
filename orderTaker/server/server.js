const express = require('express')
const shell = require('shelljs')
var fs = require("fs")
const dotenv = require('dotenv');
const dotenvExpand = require('dotenv-expand');
const path = require('path');
const envPath = path.resolve(__dirname, '../../', '.env');

dotenvExpand.expand(dotenv.config({ path: envPath }));

function WriteLink(file, link){
    fs.appendFile(file, `${link}\n`, function(err){
    if (err){
        console.log(`faile to write ${link} in ${file}`)
    } else {
        console.log("link succesfully written !")
    }
    })
}

function ReadLinkAndMoveIt(fileSrc, fileDst){
    const data = fs.readFileSync(fileSrc, 'utf8');
    const linksArray = data.split("\n");
    const linesExceptFirst = linksArray.slice(1).join('\n');
    
    if(linksArray[0] !== '')
        WriteLink(fileDst, linksArray[0]);

    fs.writeFileSync(fileSrc, linesExceptFirst);

    return linksArray[0];
}

const app = express()
app.use(express.json())


app.post("/test", (req, res) => {
    const link = req.body.link;
    const template = req.body.template;
    const addLinkPool = req.body.addLinkPool
    const createFromLinkPool = req.body.createFromLinkPool
    const createOriginalContent = req.body.createOriginalContent
    const createScriptFromLink = req.body.createScriptFromLink
    const createScriptFromInput = req.body.createScriptFromInput
    const scriptNumber = req.body.scriptNumber
    const wordNumber = req.body.wordNumber

    if (addLinkPool && link !== '') {
        // console.log(`${process.env.LINKS_FOLDER_PATH}/${template}-links.txt`)
        // WriteLink(`${process.env.LINKS_FOLDER_PATH}/${template}-links.txt`, link);
        WriteLink("link.txt", link);
    }
    else if (createFromLinkPool && !addLinkPool){
        const linkPool = ReadLinkAndMoveIt("link.txt", "link-used.txt");
        // const linkPool = ReadLinkAndMoveIt(`${process.env.LINKS_FOLDER_PATH}/${template}-links.txt`, `${process.env.LINKS_FOLDER_PATH}/${template}-links-used.txt`,);
        console.log(`create from pool link: ${linkPool}`)
        // shell.exec(`../../automate.sh ${template} ${linkPool}`)
    }
    else if (createOriginalContent){
        console.log("create original content")
    }
    else if (createScriptFromLink && link != '') {
        shell.exec(`../../test.sh ${template} ${link}`)
    }
    else
        // shell.exec(`../../automate.sh ${template} ${link}`)
    console.log(req.body);
})

app.listen(5000, () => {console.log(`Server started on port 5000`)})