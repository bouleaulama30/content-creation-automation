import React, {useState} from 'react'

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

function MyForm() {
  const [link, setLink] = useState("");
  const [template, setTemplate] = useState("default");
  const [addLinkPool, setAddLinkPool] = useState(false);
  const [createFromLinkPool, setcreateFromLinkPool] = useState(false);
  const [createOriginalContent, setcreateOriginalContent] = useState(false);
  const [createScriptFromLink, setcreateScriptFromLink] = useState(false);
  const [createScriptFromInput, setcreateScriptFromInput] = useState(false);
  const [scriptNumber, setscriptNumber] = useState(false);
  const [wordNumber, setwordNumber] = useState(false);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      link: link,
      template: template,
      addLinkPool: addLinkPool,
      createFromLinkPool: createFromLinkPool,
      createOriginalContent: createOriginalContent,
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
    }catch(err){
      console.error()
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
          placeholder=" Enter number of script"
          type="number"
          onChange={handlescriptNumber}
        />      
      </div>
      <div className="form-row">
        <input
          id="numberOfWord"
          placeholder=" Enter number of word"
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

function App() {

  return (
    <div>
      <h1>Content Creation Automation</h1>
      <MyForm />
    </div>
  )
}
export default App