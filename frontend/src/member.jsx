import React, { Component } from 'react';
// import { Container, Table } from 'reactstrap';
// import 'bootstrap/dist/css/bootstrap.css';




class Member extends Component {

	constructor(props) {
		super(props);
		this.state = { members: [] };
	}

	componentDidMount() {
		fetch('http://localhost:8000/myapp/todo').then(response => response.json())
			.then(data => this.setState({
				
				members: data["data"]

			}));
	}

	render() {
		const { members } = this.state;


		members.forEach(item => console.log(item));



		
		const memberList = members.map(member => {
			return <tr key={member.id}>
                <td>{member.item}</td>
				</tr>
		});
		// let data = ['apples', 'bananas', 'oranges', 'grapes']
		// let newArray = data.map(item => {
		// 	// do something here ...
		// 	return item
		// 	})
		// console.log(newArray)
		return (
			<div>
				<table>
					<tbody>{memberList}</tbody>
				</table>
				
			</div>
		);
	}

}
export default Member;