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
		fetch('/api/applications/')
			.then(response => response.json())
			.then(data => setApplications(data))
	}, [])

	function createApplication(event) {
		event.preventDefault()

		const url = editingApplicationId
			? `/api/applications/${editingApplicationId}`
			: '/api/applications/'

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
		fetch(`/api/applications/${applicationId}`, {
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
			company_name: application.company_name,
			career_url: application.career_url ?? '',
			job_title: application.job_title,
			job_url: application.job_url ?? '',
			role_type: application.role_type ?? '',
			employment_type: application.employment_type ?? '',
			work_location: application.work_location ?? '',
			location: application.location ?? '',
			status: application.status,
			notes: application.notes ?? '',
			date_applied: application.date_applied ?? ''
		})

		setShowModal(true)
	}

	return (
		<div>
			<h1>Internship Tracker</h1>
			
			<button 
			className="add-application-button"
			onClick={() => {
				setEditingApplicationId(null)
				setNewApplication({
					company_name: '',
					career_url: '',
					job_title: '',
					job_url: '',
					employment_type: '',
					work_location: '',
					location: '',
					status: '',
					notes: '',
					date_applied: ''
				})
				setShowModal(true)
			}}>
				Add Application
			</button>

			{showModal && (
				<div className="modal-overlay">
					<div className="modal">
						<form className="application-form" onSubmit={createApplication}>
							<h2>{editingApplicationId ? 'Edit Application' : 'Add Application'}</h2>

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
								{editingApplicationId ? 'Save Changes' : 'Add Application'}
							</button>

							<button  type="button" onClick={() => {
								setShowModal(false)
								setEditingApplicationId(null)
							}}>
								Cancel
							</button>
						</form>
					</div>
				</div>
			)}
			
			<h2>Applications</h2>

			{applications.map(application => (
				<div className="application-card" key={application.id}>
					<h3>{application.company_name} - {application.job_title}</h3>
					<p>Status: {application.status}</p>
					<p>Date Applied: {application.date_applied}</p>
					<p>Notes: {application.notes}</p>

					<p>Location: {application.location}</p>
					<p>Work Location: {application.work_location}</p>

					<p>Role Type: {application.role_type}</p>
					<p>Employment Type: {application.employment_type}</p>

					<p>Career URL: {application.career_url}</p>
					<p>Job URL: {application.job_url}</p>

					<button onClick={() => editApplication(application)}>
						Edit
					</button>

					<button onClick={() => deleteApplication(application.id)}>
						Delete
					</button>
				</div>
			))}
		</div>
	)
}

export default App
