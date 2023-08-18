import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { Sample } from '../interfaces/sample';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SampleService {
  private samplesUrl = 'http://localhost:7999';  // URL to web api
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }
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
  
  /** GET Samples from the server */
  getSampleList(): Observable<string[]> {
    const url = `${this.samplesUrl}/searching/sample-list`;
    console.log(this.http.get(url) )

    return this.http.get<string[]>(url)
      .pipe(
        tap(_ => this.log('fetched sample list')),
        catchError(this.handleError<string[]>('getSampleList', []))
      );
      
  }

  /** GET sample by serialNum. Will 404 if serialNum not found */
  getSample(serialNum: string): Observable<Sample> {
    const url = `${this.samplesUrl}/sample/${serialNum}`;
    return this.http.get<Sample>(url).pipe(
      tap(_ => this.log(`fetched sample s/n=${serialNum}`)),
      catchError(this.handleError<Sample>(`getSample s/n=${serialNum}`))
    );
  }

  /* GET samples whose serialNum contains search term */
  searchSamples(term: string): Observable<Sample[]> {
    if (!term.trim()) {
      // if not search term, return empty hero array.
      return of([]);
    }
    return this.http.get<Sample[]>(`${this.samplesUrl}/searching/samples?name=${term}`).pipe(
      tap((x) =>
        x.length
          ? this.log(`found samples matching "${term}"`)
          : this.log(`no samples matching "${term}"`)
      ),
      catchError(this.handleError<Sample[]>('searchHeroes', []))
    );
  }

}
