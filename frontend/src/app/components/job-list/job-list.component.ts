import { Component } from '@angular/core';
import { JobHeader } from 'src/app/interfaces/job_header';
import { JobService } from '../../services/job.service';

@Component({
  selector: 'app-job-list',
  templateUrl: './job-list.component.html',
  styleUrls: ['./job-list.component.css'],
})
export class JobListComponent {
  headers: JobHeader[] = [];

  constructor(private jobService: JobService) { }

  ngOnInit(): void {
    this.getHeader();
  }

  getHeader(): void {
    this.jobService.getJobs()
    .subscribe(headers => this.headers = headers);
  }
}
