import { Component, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { environment as env } from '../environments/environment';
import { IonicModule } from '@ionic/angular';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';
import { HeaderComponent } from './components/header/header.component';
import { MatInput } from '@angular/material/input';
import { MatSidenav, MatSidenavContainer, MatSidenavContent } from '@angular/material/sidenav';
import { LayoutComponent } from './components/layout/layout.component';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, 
    IonicModule, 
    HeaderComponent, LayoutComponent,
    MatSidenav, MatSidenavContainer, MatSidenavContent, 
    MatFormField, MatInput, MatSelect, MatOption, MatLabel,
    MatIcon,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent {

  constructor() { }
  
}