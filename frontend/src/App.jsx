import { useEffect, useState } from 'react'

function App() {
	const [applications, setApplications] = useState([])

	const [showModal, setShowModal] = useState(false)

	const [newApplication, setNewApplication] = useState({
		company_name: '',
		career_url: '',
		job_title: '',
		job_url: '',
		role_type: '',
		employment_type: '',
		work_location: '',
		location: '',
		status: '',
		notes: '',
		date_applied: ''
	})

	const [editingApplicationId, setEditingApplicationId] = useState(null)

	useEffect(() => {
		fetch('http://localhost:8000/applications/')
			.then(response => response.json())
			.then(data => setApplications(data))
	}, [])

	function createApplication(event) {
		event.preventDefault()

		const url = editingApplicationId
			? `http://localhost:8000/applications/${editingApplicationId}`
			: 'http://localhost:8000/applications/'

		const method = editingApplicationId ? 'PUT' : 'POST'

		fetch(url, {
			method: method,
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				...newApplication,
				date_applied: newApplication.date_applied || null
			})
		})
			.then(response => response.json())
			.then(data => {
				if (editingApplicationId) {
					setApplications(
						applications.map(application =>
							application.id === editingApplicationId ? data : application
						)
					)
				} else {
					setApplications([...applications, data])
				}

				setEditingApplicationId(null)

				setNewApplication({
					company_name: '',
					career_url: '',
					job_title: '',
					job_url: '',
					role_type: '',
					employment_type: '',
					work_location: '',
					location: '',
					status: '',
					notes: '',
					date_applied: ''
				})

				setShowModal(false)
			})
	}

	function deleteApplication(applicationId) {
		fetch(`http://localhost:8000/applications/${applicationId}`, {
			method: 'DELETE'
		})
			.then(() => {
				setApplications(
					applications.filter(application => application.id !== applicationId)
				)
			})
	}

	function editApplication(application) {
		setEditingApplicationId(application.id)

		setNewApplication({
			job_id: application.job_id,
			status: application.status,
			notes: application.notes,
			date_applied: application.date_applied
		})
	}

	return (
		<div>
			<h1>Internship Tracker</h1>
			
			<button onClick={() => setShowModal(true)}>
				Add Application
			</button>

			{showModal && (
				<div>
					<div>
						<form onSubmit={createApplication}>
							<h2>Add Application</h2>

							<input
								type="text"
								placeholder="Company Name"
								value={newApplication.company_name}
								onChange={event =>
									setNewApplication({
										...newApplication,
										company_name: event.target.value
									})
								}
							/>

							<input
								type="url"
								placeholder="Career URL"
								value={newApplication.career_url}
								onChange={event =>
									setNewApplication({
										...newApplication,
										career_url: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Job Title"
								value={newApplication.job_title}
								onChange={event =>
									setNewApplication({
										...newApplication,
										job_title: event.target.value
									})
								}
							/>

							<input
								type="url"
								placeholder="Job URL"
								value={newApplication.job_url}
								onChange={event =>
									setNewApplication({
										...newApplication,
										job_url: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Role Type"
								value={newApplication.role_type}
								onChange={event =>
									setNewApplication({
										...newApplication,
										role_type: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Employment Type"
								value={newApplication.employment_type}
								onChange={event =>
									setNewApplication({
										...newApplication,
										employment_type: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Work Location"
								value={newApplication.work_location}
								onChange={event =>
									setNewApplication({
										...newApplication,
										work_location: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Location"
								value={newApplication.location}
								onChange={event =>
									setNewApplication({
										...newApplication,
										location: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Status"
								value={newApplication.status}
								onChange={event =>
									setNewApplication({
										...newApplication,
										status: event.target.value
									})
								}
							/>

							<input
								type="text"
								placeholder="Notes"
								value={newApplication.notes}
								onChange={event =>
									setNewApplication({
										...newApplication,
										notes: event.target.value
									})
								}
							/>

							<input
								type="datetime-local"
								value={newApplication.date_applied}
								onChange={event =>
									setNewApplication({
										...newApplication,
										date_applied: event.target.value
									})
								}
							/>

							<button type="submit">
								Add Application
							</button>

							<button  type="button" onClick={() => setShowModal(false)}>
								Cancel
							</button>
						</form>
					</div>
				</div>
			)}
			
			<h2>Applications</h2>

			{applications.map(application => (
				<div key={application.id}>
					<p>Application ID: {application.id}</p>
					<p>Job ID: {application.job_id}</p>
					<p>Status: {application.status}</p>
					<p>Date Applied: {application.date_applied}</p>
					<p>Notes: {application.notes}</p>

					<button onClick={() => deleteApplication(application.id)}>
						Delete
					</button>

					<button onClick={() => editApplication(application)}>
						Edit
					</button>
				</div>
			))}
		</div>
	)
}

export default App
