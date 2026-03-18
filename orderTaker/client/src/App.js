import React, {useState} from 'react'

function MyForm() {
  const [link, setLink] = useState("");
  const [template, setTemplate] = useState("");

  const handleLink = (e) => {
    setLink(e.target.value);
  }

  const handleTemplate = (e) => {
    setTemplate(e.target.value);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      link: link,
      template: template,
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
          <input
            placeholder=" Enter Link"
            type="url"
            onChange={handleLink}
          />
          <input
            placeholder=" Enter Template"
            type="text"
            onChange={handleTemplate}
          />
          <button type="submit">
            Create
          </button>
        </form>
  );
}

function App() {

  // const [backendData, setBackenData] = useState([{}])

  // useEffect(() => {
  //   fetch("/api").then(
  //     response => response.json()
  //   ).then(
  //     data => {
  //       setBackenData(data)
  //     }
  //   )
  // }, [])

  return (
    <div>
      <h1>Welcome to content creation automation</h1>
      <MyForm />
    </div>
  )
}

      // {(typeof backendData.users === 'undefined') ? (
      //   <p>Loading...</p>
      // ): (
      //   backendData.users.map((user, i) => 
      //     <p key={i}>{user}</p>
      //   )
      // )}
export default App