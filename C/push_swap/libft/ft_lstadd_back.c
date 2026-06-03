/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 01:02:53 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/13 01:48:20 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>
//#include <stddef.h>

void	ft_lstadd_back(t_list **lst, t_list *new)
{
	t_list	*last;

	if (!lst || !new)
		return ;
	if (*lst == NULL)
	{
		*lst = new;
		return ;
	}
	last = ft_lstlast(*lst);
	last->next = new;
}

/*int	main(void)
{
	t_list	*head = NULL;
	t_list	*temp;
	int		v1 = 1, v2 = 2, v3 = 3;

	ft_lstadd_back(&head, ft_lstnew(&v1));
	ft_lstadd_back(&head, ft_lstnew(&v2));
	ft_lstadd_back(&head, ft_lstnew(&v3));
	temp = head;
	while (temp)
	{
		printf("%d -> ", *(int *)(temp->content));
		temp = temp->next;
	}
	printf("NULL\n");

	return (0);
}*/