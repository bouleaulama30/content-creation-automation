import React, {useState, useEffect} from 'react'
import './App.css';

function CheckBox({id, setState, checked}){
  const handleEvent = (e) => {
    setState(e.target.checked);
  }

  return (
      <input 
    id={id}
    type="checkbox"
    onChange={handleEvent}
    checked={checked}
    />
  )
}

function MyFormAutomation({onSubmitted}) {
  const defaultNumberOfWords = 30;
  const defaultNumberOfScripts = 1;

  const [link, setLink] = useState("");
  const [template, setTemplate] = useState("default");
  const [LANG, setLANG] = useState("fr");
  const [addLinkPool, setAddLinkPool] = useState(false);
  const [createFromLinkPool, setcreateFromLinkPool] = useState(false);
  const [createOriginalContent, setcreateOriginalContent] = useState(false);
  const [createScriptFromViralLinkPool, setcreateScriptFromViralLinkPool] = useState(false);
  const [createScriptFromLink, setcreateScriptFromLink] = useState(false);
  const [createScriptFromInput, setcreateScriptFromInput] = useState("");
  const [scriptNumber, setscriptNumber] = useState(defaultNumberOfScripts);
  const [wordNumber, setwordNumber] = useState(defaultNumberOfWords);

  const handleLink = (e) => {
    setLink(e.target.value);
  }

  const handlecreateScriptFromInput = (e) => {
    setcreateScriptFromInput(e.target.value);
  }

  const handlescriptNumber = (e) => {
    setscriptNumber(e.target.value);
  }
  const handlewordNumber = (e) => {
    setwordNumber(e.target.value);
  }
 
  const handleTemplate = (e) => {
    setTemplate(e.target.value);
  }
  const handleLANG = (e) => {
    setLANG(e.target.value);
  }
  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      link: link,
      template: template,
      LANG: LANG,
      addLinkPool: addLinkPool,
      createFromLinkPool: createFromLinkPool,
      createOriginalContent: createOriginalContent,
      createScriptFromViralLinkPool: createScriptFromViralLinkPool,
      createScriptFromLink: createScriptFromLink,
      createScriptFromInput: createScriptFromInput,
      scriptNumber: scriptNumber,
      wordNumber: wordNumber
    };
    try {
      const add = await fetch("/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });
      console.log(add)
      onSubmitted();
    }catch(err){
      console.error(err);
    };
    }
  return (
    <form className="content-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label htmlFor="link">Link: </label>
        <input
          id="link"
          placeholder=" Enter Link"
          type="url"
          onChange={handleLink}
        />
      </div>

      <div className="form-row">
        <label htmlFor="template">Template: </label>
        <select
          id="template"
          placeholder=" Enter Template"
          type="text"
          onChange={handleTemplate}
        >
          <option value="default">default</option>
          <option value="oogway">oogway</option>
          <option value="joker">joker</option>
        </select>
      </div>
      <div className="form-row">
        <label htmlFor="LANG">Language: </label>
        <select
          id="LANG"
          placeholder=" Enter Language"
          type="text"
          onChange={handleLANG}
        >
          <option value="fr">French</option>
          <option value="en">English</option>
        </select>
      </div>

      <div className="form-row checkbox-row">
        <label htmlFor="addLinkPool">Add link to pool: </label>
        <CheckBox id="addLinkPool" setState={setAddLinkPool} checked={addLinkPool}/>
      </div>
 
      <div className="form-row checkbox-row">
        <label htmlFor="createFromLinkPool">Create from link pool: </label>
        <CheckBox id="createFromLinkPool" setState={setcreateFromLinkPool} checked={createFromLinkPool}/>
      </div>

      <div className="form-row checkbox-row">
        <label htmlFor="createOriginalContent">Create original content: </label>
        <CheckBox id="createOriginalContent" setState={setcreateOriginalContent} checked={createOriginalContent}/>
      </div>

      <div className="form-row checkbox-row">
        <label htmlFor="createScriptFromViralLinkPool">Create script from viral link pool: </label>
        <CheckBox id="createScriptFromViralLinkPool" setState={setcreateScriptFromViralLinkPool} checked={createScriptFromViralLinkPool}/>
      </div>

      <div className="form-row checkbox-row">
        <label htmlFor="createScriptFromLink">Create script from link: </label>
        <CheckBox id="createScriptFromLink" setState={setcreateScriptFromLink} checked={createScriptFromLink}/>
      </div>

      <div className="form-row">
        <label htmlFor="createScriptFromInput">Create script from input: </label>
        <input
          id="input"
          placeholder=" Enter input"
          type="text"
          onChange={handlecreateScriptFromInput}
        />      
      </div>
      <div className="form-row">
        <label htmlFor="createScriptFromInput">Script parameters: </label>
      </div>
      <div className="form-row">
        <input
          id="numberOfScript"
          placeholder={` Nbr of scripts (default ${defaultNumberOfScripts})`}
          type="number"
          onChange={handlescriptNumber}
        />      
      </div>
      <div className="form-row">
        <input
          id="numberOfWord"
          placeholder={` Nbr of words (default ${defaultNumberOfWords})`}
          type="number"
          onChange={handlewordNumber}
        />      
      </div>
      <button className="form-row" type="submit">
        Create content
      </button>
    </form>
  );
}


function MyFormControl() {
  const defaultScriptLine = 0


  const [template, setTemplate] = useState("default");
  const [showScriptContentFile, setshowScriptContentFile] = useState(false);
  const [showLinkContentFile, setshowLinkContentFile] = useState(false);
  const [deleteAllContentFile, setdeleteAllContentFile] = useState(false);
  const [scriptFile, setScriptFile] = useState("")
  const [scriptLine, setScriptLine] = useState(defaultScriptLine)
  const [LANG, setLANG] = useState("fr");


  const handleLANG = (e) => {
    setLANG(e.target.value);
  }
 
  const handleTemplate = (e) => {
    setTemplate(e.target.value);
  }

  const handleScriptLine = (e) => {
    setScriptLine(e.target.value);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      template: template,
      LANG: LANG,
      showScriptContentFile: showScriptContentFile,
      showLinkContentFile: showLinkContentFile,
      deleteAllContentFile: deleteAllContentFile,
      scriptLine: scriptLine,
    };
    try {
      const getData= async() => {
        const response = await fetch("/control", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(userData),
        });
        const text = await response.text();
        setScriptFile(text);
    }
    getData();
    }catch(err){
      console.error(err);
    };
    }

  return (
    <div>
    <form className="content-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label htmlFor="template">Template: </label>
        <select
          id="template"
          placeholder=" Enter Template"
          type="text"
          onChange={handleTemplate}
        >
          <option value="default">default</option>
          <option value="oogway">oogway</option>
          <option value="joker">joker</option>
        </select>
      </div>
      <div className="form-row">
        <label htmlFor="language">Language: </label>
        <select
          id="language"
          placeholder=" Enter language"
          type="text"
          onChange={handleLANG}
        >
          <option value="fr">French</option>
          <option value="en">English</option>
        </select>
      </div>

      <div className="form-row checkbox-row">
        <label htmlFor="showScriptContentFile">Show script content file: </label>
        <CheckBox id="showScriptContentFile" setState={setshowScriptContentFile} checked={showScriptContentFile}/>
      </div>
      <div className="form-row checkbox-row">
        <label htmlFor="showLinkContentFile">Show link content file: </label>
        <CheckBox id="showLinkContentFile" setState={setshowLinkContentFile} checked={showLinkContentFile}/>
      </div>
      <div className="form-row checkbox-row">
        <label htmlFor="deleteAllContentFile">Delete all scripts in file: </label>
        <CheckBox id="deleteAllContentFile" setState={setdeleteAllContentFile} checked={deleteAllContentFile}/>
      </div>
      <div className="form-row">
        <input
          id="scriptLine"
          placeholder={` Line to delete (default ${scriptLine})`}
          type="number"
          onChange={handleScriptLine}
        />      
      </div>  
      <button className="form-row" type="submit">
        Control content
      </button>
    </form>
    <section className="logs-panel" aria-label="Execution logs">
      <h2 className="logs-title">Scrips/Links output file</h2>
      <pre className="logs-output">{scriptFile}</pre>
    </section>
    </div>
  );
}

function Logs ({refreshKey}) {
  const [log, setLog] = useState("")

  useEffect(()=>{
    const getData= async() => {
      const response = await fetch("/logs")
      const text = await response.text();
      setLog(text);
    }
    getData();
  }, [refreshKey]);

  return (
    <section className="logs-panel" aria-label="Execution logs">
      <h2 className="logs-title">Logs</h2>
      <pre className="logs-output">{log}</pre>
    </section>
  )
}

function App() {
  const [logsRefreshKey, setLogsRefreshKey] = useState(0);

  const handleSubmitComplete = () => {
    setLogsRefreshKey((prev) => prev + 1);
  }

  return (
    <div>
      <h1>Content Creation Automation</h1>
      <MyFormAutomation onSubmitted={handleSubmitComplete} />
      <Logs refreshKey={logsRefreshKey} />
    </div>
  )
}

function Control(){
return(
  <div>
    <h1>Control script panel</h1>
    <MyFormControl/>
  </div>
  )
}

export default App;
export { Control };
