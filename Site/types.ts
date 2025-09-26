export type Job = {
    jobvite_id: string;
    job_title: string;
    job_description: string;
}

export type JobsResponse = {
    jobs: Job[];
    last_updated: string;
}