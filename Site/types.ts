export type Job = {
    jobviteId: string;
    jobTitle: string;
    jobDescription: string;
    sector: string;
    workMode: string;
    country: string;
}

export type JobsResponse = {
    jobs: Job[];
    lastUpdated: string;
}