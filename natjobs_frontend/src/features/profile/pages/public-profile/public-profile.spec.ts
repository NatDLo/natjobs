import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { AuthService } from '../../../../core/services/auth.service';

import { PublicProfileComponent } from './public-profile';

describe('PublicProfileComponent', () => {
	let component: PublicProfileComponent;
	let fixture: ComponentFixture<PublicProfileComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [PublicProfileComponent],
			providers: [
				provideHttpClient(),
				{
					provide: ActivatedRoute,
					useValue: {
						paramMap: of(convertToParamMap({ id: '1' })),
						snapshot: {
							params: {
								id: '1',
							},
						},
					},
				},
				{
					provide: AuthService,
					useValue: {
						user: () => null,
						getPublicProfile: () => of({ id: 1, username: 'test', role: 'seeker' }),
					},
				},
			],
		}).compileComponents();

		fixture = TestBed.createComponent(PublicProfileComponent);
		component = fixture.componentInstance;
		await fixture.whenStable();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
