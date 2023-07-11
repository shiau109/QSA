import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SampleDetailComponent } from './components/sample-detail/sample-detail.component';
import { SearchSampleComponent } from './components/search-sample/search-sample.component';
import { JobListComponent } from './components/job-list/job-list.component';
import { SearchComponent } from './components/search/search.component';
import { JobDetailComponent } from './components/job-detail/job-detail.component'
import { JobFilterComponent } from './components/job-filter/job-filter.component';

const routes: Routes = [
  { path: '', redirectTo: '/search', pathMatch: 'full' },
  { path: 'search', component: SearchComponent },
  { path: 'search_job', component: JobFilterComponent },
  { path: 'sample/:serialNum', component: SampleDetailComponent },
  { path: 'joblist', component: JobListComponent },
  { path: 'job/:jobId', component: JobDetailComponent },

];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}