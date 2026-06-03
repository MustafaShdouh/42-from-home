/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstiter.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 01:31:00 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/13 01:48:20 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>

void	ft_lstiter(t_list *lst, void (*f)(void *))
{
	if (!lst || !f)
		return ;
	while (lst)
	{
		f(lst->content);
		lst = lst->next;
	}
}

/*void	print_node(void *content)
{
	printf("Node Content: %d\n", *(int *)content);
}

void	add_one(void *content)
{
	*(int *)content += 1;
}

int	main(void)
{
	t_list	*head = NULL;
	int		v1 = 41, v2 = 42;

	ft_lstadd_back(&head, ft_lstnew(&v1));
	ft_lstadd_back(&head, ft_lstnew(&v2));
	printf("--- First Pass (Printing) ---\n");
	ft_lstiter(head, print_node);
	printf("\n--- Modifying (Adding 1) ---\n");
	ft_lstiter(head, add_one);
	printf("\n--- Second Pass (Verify Change) ---\n");
	ft_lstiter(head, print_node);
}*/