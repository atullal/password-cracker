import logo from './logo.svg';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import './App.css';
import { useEffect, useState } from 'react';
import { getAvailableClients, submitForm } from './Api';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import ProgressBar from 'react-bootstrap/ProgressBar';

function App() {
  const [md5, setMd5] = useState("");
  const [availableClients, setAvailableClients] = useState([]);
  const [selectedClients, setSelectedClients] = useState([]);
  const [result, setResult] = useState();
  const { sendMessage, lastMessage, readyState } = useWebSocket('ws://127.0.0.1:5000/password');
  const [messageHistory, setMessageHistory] = useState([]);
  const [err, setErr] = useState();
  const [requestId, setRequestId] = useState();
  const [progress, setProgress] = useState(10);

  useEffect(() => {
    getAvailableClients().then((res) => {
      setAvailableClients(res.data["available_clients"]);
    }) 
  }, [])

  useEffect(() => {
    if (lastMessage !== null) {
      console.log(lastMessage);
      console.log(lastMessage.data);
      try {
        let response = JSON.parse(lastMessage.data.replace(/'/g, '"'));
        console.log(response);
        if(response.err) {
          setErr(response.err);
        }
        if(response.password) {
          setResult(response.password);
          setProgress(100);
        }
      } catch (error) {
        
      }
      setMessageHistory((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage, setMessageHistory]);

  const md5Input = (e) => {
    setMd5(e.target.value);
  };

  const onSubmit = (e) => {
    e.preventDefault();
    submitForm(md5, selectedClients).then((response) => {
      if(response.data.err) {
        setErr(response.data.err);
      }
      if(response.data.success) {
        setRequestId(response.data.success);
        sendMessage(JSON.stringify({
          "request_id": response.data.success
        }));
      } else {
        setErr("Something went wrong.");
      }
    });
  }

  const onCheckboxChange = (e, client) => {
    const clientFoundInd = selectedClients.findIndex((selectedClient) => selectedClient === client);
    
    if(clientFoundInd !== -1) {
      setSelectedClients(selectedClients.splice(clientFoundInd, 1))
    } else {
      setSelectedClients([...selectedClients, client])
    }
  }

  const socketTest = () => {
    sendMessage(JSON.stringify({"hello": "world"}));
  }

  return (
    <div className="App">
      <div className='container'>
        <div className='top-margin'>
          <div className='row'>
            <div className='col-md-4'></div>
            <div className='col-md-4'>
              <h1 className='app-header'>Password Cracker</h1>
              {
                !requestId ? <Form onSubmit={(e) => {onSubmit(e)}}>
                  <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>MD5 Hash</Form.Label>
                    <Form.Control type="text" placeholder="Enter hash"  onChange={(e)=>{md5Input(e)}} />
                  </Form.Group>
                  <div className='available-clients'>
                    <Form.Group className="mb-3" controlId="formClients">
                      <Form.Label>Clients</Form.Label>
                      {availableClients.map((client, ind) => {
                        return (<Form.Check 
                          key={ind}
                          onChange={(e) => {onCheckboxChange(e, client)}}
                          disabled={client.inUse}
                          type='checkbox'
                          id={`default-${ind}`}
                          label={`Client: ${client.address}, Port: ${client.port}`}
                        />);
                      })}
                    </Form.Group>
                  </div>
                  <Button className="mt-3 submit-button" variant="light" type="submit">
                  →
                  </Button>
                </Form> : <div>
                  <ProgressBar animated now={progress} />
                </div>
              }
            </div>
            <div className='col-md-4'>
            </div>
          </div>
        </div>
      </div>
    
    </div>
  );
}

export default App;
