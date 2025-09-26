import axios from 'axios'
import type { Job, JobsResponse } from '../../types'

const api = axios.create({
    baseURL: '',
})

let jobs: JobsResponse

export const getJobs = async () : Promise<JobsResponse> => {
    if (!jobs) {
        const response = await api.get('/jobs.json');
        jobs = response.data;
    }

    return jobs;
}

export const getJob = async (id: string) : Promise<Job | null> => {
    const jobs = await getJobs();
    const job = jobs.jobs.find((job) => job.jobvite_id === id);
    return job || null;
}