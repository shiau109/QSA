import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SampleDetailComponent } from './components/sample-detail/sample-detail.component';
import { SearchSampleComponent } from './components/search-sample/search-sample.component';
import { JobListComponent } from './components/job-list/job-list.component';
import { SearchComponent } from './components/search/search.component';


const routes: Routes = [
  { path: '', redirectTo: '/search', pathMatch: 'full' },
  { path: 'search', component: SearchComponent },
  { path: 'sample/:serialNum', component: SampleDetailComponent },
  { path: 'joblist', component: JobListComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}