import React, {useState} from 'react'

function MyForm() {
  const [link, setLink] = useState("");
  const [template, setTemplate] = useState("default");
  const [addLinkPool, setAddLinkPool] = useState(false);
  const [createFromLinkPool, setcreateFromLinkPool] = useState(false);
  const [createOriginalContent, setcreateOriginalContent] = useState(false);

  const handleLink = (e) => {
    setLink(e.target.value);
  }
 
  const handleTemplate = (e) => {
    setTemplate(e.target.value);
  }

  const handleAddLinkPool = (e) => {
    setAddLinkPool(e.target.checked);
  }

  const handlecreateFromLinkPool = (e) => {
    setcreateFromLinkPool(e.target.checked);
  }

  const handlecreateOriginalContent = (e) => {
    setcreateOriginalContent(e.target.checked);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      link: link,
      template: template,
      addLinkPool: addLinkPool,
      createFromLinkPool: createFromLinkPool,
      createOriginalContent: createOriginalContent
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
    <form onSubmit={handleSubmit}>
          <label for="link">Link: </label>
          <input
            id="link"
            placeholder=" Enter Link"
            type="url"
            onChange={handleLink}
          />
          <br></br>
          <br></br>
          <label for="template">Template: </label>
          <select
            id="template"
            placeholder=" Enter Template"
            type="text"
            onChange={handleTemplate}
          >
          <option value="default">default</option>
          <option value="oogway">oogway</option>
          </select>
          <br></br>
          <label for="addLinkPool">Add link to pool: </label>
          <input 
            id="addLinkPool"
            type="checkbox"
            onChange={handleAddLinkPool}
            checked={addLinkPool}
          />
          <br></br>
          <label for="createFromLinkPool">Create from link pool: </label>
          <input 
            id="createFromLinkPool"
            type="checkbox"
            onChange={handlecreateFromLinkPool}
            checked={createFromLinkPool}
          />
          <br></br>
          <label for="createOriginalContent">Create original content: </label>
          <input 
            id="createOriginalContent"
            type="checkbox"
            onChange={handlecreateOriginalContent}
            checked={createOriginalContent}
          />
          <br></br>
          <button type="submit">
            Create content
          </button>
        </form>
  );
}

function App() {

  return (
    <div>
      <h1>Welcome to content creation automation</h1>
      <MyForm />
    </div>
  )
}
export default App