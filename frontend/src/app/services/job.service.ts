import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { Sample } from '../interfaces/sample';
import { JobHeader } from '../interfaces/job_header';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { catchError, map, tap } from 'rxjs/operators';
import { JobFilter } from '../interfaces/filter';

@Injectable({
  providedIn: 'root'
})
export class JobService {

  private dataUrl = 'http://localhost:8000';  // URL to web api
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  data!:JobHeader[];
  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  /** GET Jobs from the server */
  getJobs(): Observable<JobHeader[]> {
    console.log(this.http.get(this.dataUrl) )
    return this.http.get<JobHeader[]>(this.dataUrl)
      .pipe(
        tap(_ => this.log('fetched heroes')),
        catchError(this.handleError<JobHeader[]>('getHeroes', []))
      );
      
  }

  /** GET job by jobid. Will 404 if jobid not found */
  getJobDetail(jobId: string): Observable<JobHeader> {
    const url = `${this.dataUrl}/job/${jobId}`;
    return this.http.get<JobHeader>(url).pipe(
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<JobHeader>(`Job ID ${jobId} return error`))
    );
  }

  /** Log a SampleService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`SampleService: ${message}`);
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   *
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /* GET samples whose serialNum contains search term */
  filterJobs( filter: JobFilter): Observable<JobHeader[]> {
    // if (!filter.trim()) {
    //   // if not search term, return empty hero array.
    //   return of([]);
    // }
    // console.log(`${this.dataUrl}/search/job`)
    return this.http.post<any>(`${this.dataUrl}/search/job`,filter).pipe(
      tap(_ => this.log(`search`)),
      catchError(this.handleError<JobHeader[]>(`search error`))
    );
  }

}
