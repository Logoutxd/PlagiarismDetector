module MyModule::Crowdfunding {
    use aptos_framework::signer;
    use aptos_framework::coin;
    use aptos_framework::aptos_coin::AptosCoin;

    /// Struct representing a crowdfunding project.
    struct Project has key, store {
        owner: address,   // Project owner
        total_funds: u64, // Total tokens raised for the project
        goal: u64,        // Funding goal of the project
    }

    /// Struct to store all crowdfunding projects for an account.
    struct ProjectHolder has key, store {
        project: Project,
    }

    /// Function to create a new project with a funding goal.
    public fun create_project(owner: &signer, goal: u64) {
        let owner_address = signer::address_of(owner);
        assert!(goal > 0, 1); // Ensure goal is a valid amount

        move_to(owner, ProjectHolder {
            project: Project {
                owner: owner_address,
                total_funds: 0,
                goal,
            },
        });
    }

    /// Function for users to support the project by contributing tokens.
    public fun contribute_to_project(contributor: &signer, project_owner: address, amount: u64) acquires ProjectHolder {
        let project_holder = borrow_global_mut<ProjectHolder>(project_owner);
        let project = &mut project_holder.project;

        // Ensure the contribution does not exceed the funding goal
        assert!(project.total_funds + amount <= project.goal, 2);

        // Transfer the contribution from the contributor to the project owner
        let contribution = coin::withdraw<AptosCoin>(contributor, amount);
        coin::deposit<AptosCoin>(project_owner, contribution);

        // Update the total funds raised
        project.total_funds = project.total_funds + amount;
    }

    /// Function to check if the project is fully funded.
    public fun is_funded(project_owner: address): bool acquires ProjectHolder {
        let project_holder = borrow_global<ProjectHolder>(project_owner);
        project_holder.project.total_funds >= project_holder.project.goal
    }
}

