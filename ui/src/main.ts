import { enableProdMode, importProvidersFrom } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { environment } from './environments/environment';
import { AppComponent } from './app/app.component'; //ROUTES
import { NgxEchartsModule } from 'ngx-echarts';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { provideAnimations } from '@angular/platform-browser/animations';
import { withInterceptorsFromDi, provideHttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserModule, bootstrapApplication } from '@angular/platform-browser';
import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { ModuleRegistry } from '@ag-grid-community/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Route, RouterModule } from '@angular/router';
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { appConfig } from './app/app.config';
import 'zone.js';
import './polyfills';
import { SideNavService } from './app/services/sidenav.service';
import { ListReducer } from './app/state/list/list.reducers';

if (environment.production) {
  enableProdMode();
}

ModuleRegistry.registerModules([ClientSideRowModelModule]);

export const ROUTES: Route[] = [
  {
    path: '', 
    loadComponent: () => import('./app/components/dashboard/dashboard.component').then(mod => mod.DashboardComponent)
  },
  {
    path: '**',
    redirectTo: '',
  },
];

bootstrapApplication(AppComponent, {
    providers: [
        // {
        //   provide: ENVIRONMENT_INITIALIZER,
        // },
        importProvidersFrom([
            BrowserAnimationsModule,
            StoreModule.forRoot({}),
            StoreDevtoolsModule.instrument(),
            SideNavService,
            RouterModule.forRoot(ROUTES),
          ],
          StoreModule.forRoot({ list: ListReducer }),
          BrowserModule, FormsModule, FlexLayoutModule,
          MatToolbarModule, MatCardModule, MatButtonModule, MatIconModule,
          MatFormFieldModule, MatSelectModule, MatInputModule, 
          NgxEchartsModule.forRoot({ echarts: () => import('echarts')})),
        provideHttpClient(withInterceptorsFromDi()),
        provideAnimations(),
    ]
})
.then((ref) => {
  // @ts-ignore
  if (window['ngRef']) {
    // @ts-ignore
    window['ngRef'].destroy();
  }
  // @ts-ignore
  window['ngRef'] = ref;
})
.catch((err) => console.error(err));