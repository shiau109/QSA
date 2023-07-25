import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SampleDetailComponent } from './components/sample-detail/sample-detail.component';
import { SearchSampleComponent } from './components/search-sample/search-sample.component';
import { JobListComponent } from './components/job-list/job-list.component';
import { SearchComponent } from './components/search/search.component';
import { JobDetailComponent } from './components/job-detail/job-detail.component'
import { JobFilterComponent } from './components/job-filter/job-filter.component';
import { AnalyzerHomeComponent } from './components/analyzer-home/analyzer-home.component';
import { ResonatorAnalysisComponent } from './components/resonator-analysis/resonator-analysis.component';
const routes: Routes = [
  { path: '', redirectTo: '/search', pathMatch: 'full' },
  { path: 'search', component: SearchComponent },
  { path: 'sample/:serialNum', component: SampleDetailComponent },
  { path: 'joblist', component: JobListComponent },
  { path: 'job/:jobId', component: JobDetailComponent },
  { path: 'analyzer', component: AnalyzerHomeComponent },
  { path: 'analyzer/resonator_analysis', component: ResonatorAnalysisComponent },

];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}