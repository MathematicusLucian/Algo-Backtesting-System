import {Component, OnInit, Input} from '@angular/core';

@Component({
  selector: 'prefab-card',
  standalone: true,
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  @Input() cardData: any;
  driverImage: any;

  constructor() { }

  ngOnInit(): void {}

  formatTime(result){
    return result && result.Time && result.Time.time ? result.Time.time : "N/A";
  }

  constructImgUrl(familyName){
    const url = `https://media.formula1.com/content/dam/fom-website/drivers/2024Drivers/`+familyName+`.jpg.img.256.small.jpg/1708362100444.jpg`;
    return url;
  }
}