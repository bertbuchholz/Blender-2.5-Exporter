import bpy

class yafIntegrator:
    def __init__(self, interface):
        self.yi = interface
            
    def exportIntegrator(self, scene):
        yi = self.yi

        yi.paramsClearAll()

        yi.paramsSetInt("raydepth", scene.gs_ray_depth)
        yi.paramsSetInt("shadowDepth", scene.gs_shadow_depth)
        yi.paramsSetBool("transpShad", scene.gs_transp_shad)

        light_type = scene.intg_light_method
        yi.printInfo("Exporting Integrator:" + light_type)

        if light_type == "Direct Lighting" :
            yi.paramsSetString("type", "directlighting")

            yi.paramsSetBool("caustics", scene.intg_use_caustics )

            if scene.intg_use_caustics:
                yi.paramsSetInt("photons", scene.intg_photons)
                yi.paramsSetInt("caustic_mix", scene.intg_caustic_mix)
                yi.paramsSetInt("caustic_depth", scene.intg_caustic_depth)
                yi.paramsSetFloat("caustic_radius", scene.intg_caustic_radius)

            if scene.intg_use_AO :
                yi.paramsSetBool("do_AO", scene.intg_use_AO)
                yi.paramsSetInt("AO_samples", scene.intg_AO_samples)
                yi.paramsSetFloat("AO_distance",scene.intg_AO_distance)

                c = scene.intg_AO_color
                yi.paramsSetColor("AO_color", c[0], c[1], c[2])
            
        elif light_type == "Photon Mapping":
            yi.paramsSetString("type", "photonmapping")
            yi.paramsSetInt("fg_samples", scene.intg_fg_samples)
            yi.paramsSetInt("photons", scene.intg_photons)
            yi.paramsSetInt("cPhotons", scene.intg_cPhotons)
            yi.paramsSetFloat("diffuseRadius", scene.intg_diffuse_radius)
            yi.paramsSetFloat("causticRadius", scene.intg_caustic_radius)
            yi.paramsSetInt("search", scene.intg_search)
            yi.paramsSetBool("show_map", scene.intg_show_map)
            yi.paramsSetInt("fg_bounces", scene.intg_fg_bounces)
            yi.paramsSetInt("caustic_mix", scene.intg_caustic_mix)
            yi.paramsSetBool("finalGather", scene.intg_final_gather)
            yi.paramsSetInt("bounces", scene.intg_bounces)
#               yi.paramsSetBool("use_background", renderer["use_background"])

        elif light_type == "Pathtracing":
            yi.paramsSetString("type", "pathtracing");
            yi.paramsSetInt("path_samples", scene.intg_path_samples)
            yi.paramsSetInt("bounces", scene.intg_bounces)
            yi.paramsSetBool("no_recursive", scene.intg_no_recursion)
                    
            caus_type = scene.intg_caustic_method
            photons = False;
            #print("Caustic type is :" + caus_type )
            if caus_type == "None":
                    yi.paramsSetString("caustic_type", "none");
            elif caus_type == "Path":
                    yi.paramsSetString("caustic_type", "path");
            elif caus_type == "Photon":
                    yi.paramsSetString("caustic_type", "photon")
                    photons = True
            elif caus_type == "Path+Photon":
                    yi.paramsSetString("caustic_type", "both")
                    photons = True

            if photons:
                    yi.paramsSetInt("photons", scene.intg_photons)
                    yi.paramsSetInt("caustic_mix", scene.intg_caustic_mix)
                    yi.paramsSetInt("caustic_depth", scene.intg_caustic_depth)
                    yi.paramsSetFloat("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Bidirectional" :
            yi.paramsSetString("type", "bidirectional")
    
        elif light_type == "Debug":
            yi.paramsSetString("type", "DebugIntegrator")
            
            debugTypeStr = scene.intg_debug_type 

            if debugTypeStr == "N":
                    yi.paramsSetInt("debugType", 1);
            elif debugTypeStr == "dPdU" :
                    yi.paramsSetInt("debugType", 2);
            elif debugTypeStr == "dPdV" :
                    yi.paramsSetInt("debugType", 3);
            elif debugTypeStr == "NU" :
                    yi.paramsSetInt("debugType", 4);
            elif debugTypeStr == "NV" :
                    yi.paramsSetInt("debugType", 5);
            elif debugTypeStr ==  "dSdU" :
                    yi.paramsSetInt("debugType", 6);
            elif debugTypeStr ==  "dSdV" :
                    yi.paramsSetInt("debugType", 7);

            yi.paramsSetBool("showPN",scene.intg_show_perturbed_normals)

        elif light_type == "SPPM":
            yi.paramsSetString("type", "SPPM")
            yi.paramsSetInt("photons", scene.intg_photons)
            yi.paramsSetFloat("diffuseRadius", scene.intg_diffuse_radius)
            yi.paramsSetInt("search", scene.intg_search)
            yi.paramsSetFloat("times", scene.intg_times)
            yi.paramsSetInt("bounces", scene.intg_bounces)
            yi.paramsSetInt("passNums", scene.intg_pass_num)
            yi.paramsSetBool("pmIRE", scene.intg_pm_ire)

        elif light_type == "PBGI":
            yi.paramsSetString("type", "pbgi")
            yi.paramsSetInt("samplesPerArea", scene.intg_pbgi_samples)
            yi.paramsSetBool("debug", scene.intg_pbgi_debug)
            yi.paramsSetBool("indirectOnly", scene.intg_pbgi_indirect)
            yi.paramsSetFloat("maxSolidAngle", scene.intg_pbgi_maxSolidAngle)
            yi.paramsSetInt("debugTreeDepth", scene.intg_pbgi_debugTreeDepth)
            yi.paramsSetBool("debugOutputPointsToFile", scene.intg_pbgi_debugPointsToFile)
            yi.paramsSetString("debug_type", scene.intg_pbgi_debug_type)
            yi.paramsSetBool("render_single_pixel", scene.intg_pbgi_render_single_pixel)
            yi.paramsSetInt("pixel_x", scene.intg_pbgi_pixel_x)
            yi.paramsSetInt("pixel_y", scene.intg_pbgi_pixel_y)
            yi.paramsSetBool("do_load_gi_points", scene.intg_pbgi_do_load_gi_points)
            yi.paramsSetInt("fb_resolution", scene.intg_pbgi_fb_resolution)
            yi.paramsSetString("fb_type", scene.intg_pbgi_fb_type)


        yi.createIntegrator("default")
        return True


    def exportVolumeIntegrator(self, scene):
        yi = self.yi
        yi.paramsClearAll()

        world = scene.world

        if world:
            # preset default volume integrator
            vint_type = world.v_int_type
            yi.printInfo("Exporter: Creating Volume Integrator: \"" + vint_type + "\"...")

            if vint_type == 'Single Scatter':
                yi.paramsSetString("type", "SingleScatterIntegrator");
                yi.paramsSetFloat("stepSize", world.v_int_step_size )
                yi.paramsSetBool("adaptive", world.v_int_adaptive )
                yi.paramsSetBool("optimize", world.v_int_optimize )

            elif vint_type  == 'Sky':
                yi.paramsSetString( "type", "SkyIntegrator")
                yi.paramsSetFloat( "turbidity", world.v_int_dsturbidity )
                yi.paramsSetFloat( "stepSize", world.v_int_step_size )
                yi.paramsSetFloat( "alpha", world.v_int_alpha )
                yi.paramsSetFloat( "sigma_t", world.v_int_scale )

            else:
                yi.paramsSetString("type", "none")
        else:
             yi.paramsSetString("type", "none")

        yi.createIntegrator("volintegr")
        return True
