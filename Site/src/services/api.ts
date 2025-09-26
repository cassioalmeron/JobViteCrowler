import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

export const getJobs = async () => {
  const response = await api.get('/jobs')
  return response.data
}

export const getJob = async (id: string) => {
  const response = await api.get(`/jobs/${id}`)
  return response.data
}

export const syncJobs = async () => {
  const response = await api.post('/sync')
  return response.data
}

export default api