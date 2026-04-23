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

app.get("/logs", (req, res) => {
    console.log("logs")
    const logs = fs.readFileSync("logs.txt", "utf-8")
    res.send(logs)
    // res.send({"log": {logs}})
})

app.post("/test", (req, res) => {
    const link = req.body.link;
    const template = req.body.template;
    const addLinkPool = req.body.addLinkPool
    const createFromLinkPool = req.body.createFromLinkPool
    const createOriginalContent = req.body.createOriginalContent
    const createScriptFromViralLinkPool = req.body.createScriptFromViralLinkPool
    const createScriptFromLink = req.body.createScriptFromLink
    const createScriptFromInput = req.body.createScriptFromInput

    const dataString = JSON.stringify(req.body, null);
    fs.writeFileSync(`${process.env.DATA_CLIENT_FILE}`, dataString);

    if (addLinkPool && link !== '') {
        fs.writeFileSync("logs.txt", "Task in progress: adding link to pool...");
        console.log(`${process.env.LINKS_FOLDER_PATH}/${template}-links.txt`)
        WriteLink(`${process.env.LINKS_FOLDER_PATH}/${template}-links.txt`, link);
        fs.writeFileSync("logs.txt", "Case addLinkPool: link added to pool");
    }
    else if (createFromLinkPool && !addLinkPool){
        fs.writeFileSync("logs.txt", "Task in progress: creating content from link pool...");
        // const linkPool = ReadLinkAndMoveIt("link.txt", "link-used.txt");
        const linkPool = ReadLinkAndMoveIt(`${process.env.LINKS_FOLDER_PATH}/${template}-links.txt`, `${process.env.LINKS_FOLDER_PATH}/${template}-links-used.txt`,);
        console.log(`create from pool link: ${linkPool}`)
        shell.exec(`${process.env.PROJECT_BASE_PATH}/automate.sh ${template} ${linkPool}`)
        fs.writeFileSync("logs.txt", `Case createFromLinkPool: used link ${linkPool}`);
    }
    else if (createOriginalContent){
        fs.writeFileSync("logs.txt", "Task in progress: creating original content...");
        console.log("create original content")
        shell.exec(`${process.env.PROJECT_BASE_PATH}/content-creator.sh ${template}`);
        shell.exec(`${process.env.PROJECT_BASE_PATH}/automate.sh ${template} ${link}`)
        fs.writeFileSync("logs.txt", "Case createOriginalContent: content generated");
    }
    else if (createScriptFromViralLinkPool) {
        fs.writeFileSync("logs.txt", "Task in progress: creating script from viral link pool...");
        console.log("create script from viral link pool");
        shell.exec(`${process.env.PYTHON_PATH} ${process.env.TRIGGER_PATH}/viralLinkTrigger.py`);
        fs.writeFileSync("logs.txt", `Case createScriptFromViralLinkPool: script created from viral link ${link}`);
    }
    else if (createScriptFromLink && link != '') {
        fs.writeFileSync("logs.txt", "Task in progress: creating script from link...");
        console.log("create script from link");
        shell.exec(`${process.env.PROJECT_BASE_PATH}/script-creator.sh ${link}`);
        fs.writeFileSync("logs.txt", `Case createScriptFromLink: script created from link ${link}`);
    }
    else if (createScriptFromInput != '' && link == '') {
        fs.writeFileSync("logs.txt", "Task in progress: creating script from input...");
        console.log("create script from input");
        shell.exec(`${process.env.PYTHON_PATH} ${process.env.CREATOR_PATH}/script-creator.py`);
        fs.writeFileSync("logs.txt", "Case createScriptFromInput: script created from input");
    }
    else {
        fs.writeFileSync("logs.txt", "Task in progress: running default automation...");
        shell.exec(`${process.env.PROJECT_BASE_PATH}/automate.sh ${template} ${link}`)
        fs.writeFileSync("logs.txt", "Case default: automate script executed");
    }
    console.log(req.body);
})

app.listen(5000, () => {console.log(`Server started on port 5000`)})