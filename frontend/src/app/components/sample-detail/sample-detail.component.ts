import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { Sample } from 'src/app/interfaces/sample';
import { SampleService } from 'src/app/services/sample.service';

@Component({
  selector: 'app-sample-detail',
  templateUrl: './sample-detail.component.html',
  styleUrls: ['./sample-detail.component.css']
})
export class SampleDetailComponent implements OnInit {
  sample: Sample | undefined;

  constructor(
    private route: ActivatedRoute,
    private sampleService: SampleService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getSample();
  }

  getSample(): void {
    const sn = this.route.snapshot.paramMap.get('serialNum');
    if (sn!= null){
      this.sampleService.getSample(sn)
      .subscribe(sample => this.sample = sample);
    }

  }
  goBack(): void {
    this.location.back();
  }
  
}
