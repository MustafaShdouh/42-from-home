/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 19:05:38 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/12 19:05:38 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>

int	ft_lstsize(t_list *lst)
{
	int	count;

	count = 0;
	while (lst != NULL)
	{
		count++;
		lst = lst->next;
	}
	return (count);
}

/*int	main(void)
{
	t_list	*head = NULL;
	int		size;

	size = ft_lstsize(head);
	printf("Empty size: %d (Expected: 0)\n", size);
	ft_lstadd_front(&head, ft_lstnew(NULL));
	ft_lstadd_front(&head, ft_lstnew(NULL));
	ft_lstadd_front(&head, ft_lstnew(NULL));
	size = ft_lstsize(head);
	printf("Full size : %d (Expected: 3)\n", size);
}*/