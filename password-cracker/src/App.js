import logo from './logo.svg';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import './App.css';
import { useEffect, useState } from 'react';
import { getAvailableClients, submitForm } from './Api';

function App() {
  const [email, setEmail] = useState("");
  const [md5, setMd5] = useState("");
  const [availableClients, setAvailableClients] = useState([]);
  const [selectedClients, setSelectedClients] = useState([]);
  const [result, setResult] = useState();

  useEffect(() => {
    getAvailableClients().then((res) => {
      setAvailableClients(res.data["available_clients"]);
      console.log(res.data["available_clients"]);
    }) 
  }, [])

  const emailInput = (e) => {
    setEmail(e.target.value);
  };

  const md5Input = (e) => {
    setMd5(e.target.value);
  };

  const onSubmit = (e) => {
    e.preventDefault();
    console.log(email);
    console.log(md5);
    submitForm(email, md5, selectedClients).then((response) => {
      console.log(response);
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

  return (
    <div className="App">
      <div className='container'>
        <div className='top-margin'>
          <div className='row'>
            <div className='col-md-4'></div>
            <div className='col-md-4'>
              <h1 className='app-header'>Password Cracker</h1>
              <Form onSubmit={(e) => {onSubmit(e)}}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>Email address (optional)</Form.Label>
                  <Form.Control type="email" placeholder="Enter email" onChange={(e)=>{emailInput(e)}} />
                  <Form.Text className="text-muted">
                    You will receive the cracked password in your inbox.
                  </Form.Text>
                </Form.Group>

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
              </Form>
            </div>
            <div className='col-md-4'></div>
          </div>
        </div>
      </div>
    
    </div>
  );
}

export default App;
